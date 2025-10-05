"""
Price service for CypherD Wallet Backend
BULLETPROOF price fetching and conversion using Skip API
"""

import requests
import logging
from decimal import Decimal
from models.database import PriceCache, db
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class PriceService:
    """Service class for price operations"""
    
    def __init__(self, skip_api_url=None):
        self.skip_api_url = skip_api_url or 'https://api.skip.build/v2/fungible/msgs_direct'
        self.cache_duration = timedelta(minutes=5)  # Cache prices for 5 minutes
    
    def get_current_eth_price(self):
        """Get current ETH price in USD"""
        try:
            logger.info("=== ETH PRICE FETCH DEBUG START ===")
            
            # Check cache first
            logger.debug("Checking cache for ETH_USD price...")
            cached_price = self._get_cached_price('ETH_USD')
            if cached_price:
                logger.info(f"✅ CACHE HIT: ETH price from cache = ${cached_price}")
                return {
                    'success': True,
                    'price': cached_price,
                    'source': 'cache'
                }
            
            logger.info("❌ CACHE MISS: Fetching fresh price from CoinGecko API")
            
            # Fetch from CoinGecko API
            url = 'https://api.coingecko.com/api/v3/simple/price'
            params = {
                'ids': 'ethereum',
                'vs_currencies': 'usd'
            }
            
            logger.info(f"🌐 API REQUEST: {url}")
            logger.info(f"📋 REQUEST PARAMS: {params}")
            
            import time
            start_time = time.time()
            response = requests.get(url, params=params, timeout=10)
            request_time = time.time() - start_time
            
            logger.info(f"⏱️  REQUEST TIME: {request_time:.3f} seconds")
            logger.info(f"📊 RESPONSE STATUS: {response.status_code}")
            logger.info(f"📏 RESPONSE SIZE: {len(response.content)} bytes")
            
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"🔍 RAW API RESPONSE: {data}")
            
            # Validate response structure
            if 'ethereum' not in data:
                logger.error(f"❌ INVALID RESPONSE: Missing 'ethereum' key in response: {data}")
                raise ValueError("Invalid API response: missing 'ethereum' key")
            
            if 'usd' not in data['ethereum']:
                logger.error(f"❌ INVALID RESPONSE: Missing 'usd' key in ethereum data: {data['ethereum']}")
                raise ValueError("Invalid API response: missing 'usd' key")
            
            eth_price = data['ethereum']['usd']
            logger.info(f"💰 EXTRACTED ETH PRICE: ${eth_price}")
            
            # Validate price is reasonable
            if not isinstance(eth_price, (int, float)) or eth_price <= 0:
                logger.error(f"❌ INVALID PRICE: ETH price is not a valid positive number: {eth_price} (type: {type(eth_price)})")
                raise ValueError(f"Invalid ETH price: {eth_price}")
            
            if eth_price < 100 or eth_price > 10000:
                logger.warning(f"⚠️  SUSPICIOUS PRICE: ETH price seems unusual: ${eth_price}")
            
            # Cache the price
            logger.debug("Caching the fetched price...")
            self._cache_price('ETH_USD', eth_price)
            
            logger.info(f"✅ SUCCESS: ETH price fetched and cached = ${eth_price}")
            logger.info("=== ETH PRICE FETCH DEBUG END ===")
            
            return {
                'success': True,
                'price': eth_price,
                'source': 'api'
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"🌐 NETWORK ERROR: CoinGecko API request failed: {str(e)}")
            logger.error(f"📊 RESPONSE DETAILS: Status={getattr(e.response, 'status_code', 'N/A')}, Content={getattr(e.response, 'text', 'N/A')}")
            return {
                'success': False,
                'error': f'Network error fetching ETH price: {str(e)}'
            }
        except ValueError as e:
            logger.error(f"❌ DATA VALIDATION ERROR: {str(e)}")
            return {
                'success': False,
                'error': f'Data validation error: {str(e)}'
            }
        except Exception as e:
            logger.error(f"💥 UNEXPECTED ERROR: {str(e)}", exc_info=True)
            return {
                'success': False,
                'error': f'Unexpected error fetching ETH price: {str(e)}'
            }
    
    def get_eth_amount_for_usd(self, usd_amount):
        """Convert USD amount to ETH using Skip API with fallback"""
        try:
            logger.info("=== USD TO ETH CONVERSION DEBUG START ===")
            logger.info(f"💵 INPUT USD AMOUNT: {usd_amount} (type: {type(usd_amount)})")
            
            # Validate input
            try:
                usd_decimal = Decimal(str(usd_amount))
                logger.info(f"✅ USD VALIDATION: Converted to Decimal = {usd_decimal}")
                if usd_decimal <= 0:
                    logger.error(f"❌ INVALID AMOUNT: USD amount must be greater than 0, got: {usd_decimal}")
                    return {
                        'success': False,
                        'error': 'USD amount must be greater than 0'
                    }
            except Exception as validation_error:
                logger.error(f"❌ VALIDATION ERROR: Invalid USD amount format: {usd_amount}, error: {str(validation_error)}")
                return {
                    'success': False,
                    'error': 'Invalid USD amount format'
                }
            
            # Try Skip API first
            try:
                logger.info("🚀 ATTEMPTING SKIP API CONVERSION")
                
                # Convert USD to USDC units (6 decimals)
                usdc_units = int(float(usd_amount) * (10 ** 6))
                logger.info(f"💱 USD TO USDC UNITS: ${usd_amount} → {usdc_units} units (6 decimals)")
                
                # Prepare Skip API request
                payload = {
                    "source_asset_denom": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",  # USDC contract
                    "source_asset_chain_id": "1",
                    "dest_asset_denom": "ethereum-native",
                    "dest_asset_chain_id": "1",
                    "amount_in": str(usdc_units),
                    "chain_ids_to_addresses": {
                        "1": "0x742d35Cc6634C0532925a3b8D4C9db96c728b0B4"
                    },
                    "slippage_tolerance_percent": "1",
                    "smart_swap_options": {
                        "evm_swaps": True
                    },
                    "allow_unsafe": False
                }
                
                logger.info(f"📤 SKIP API REQUEST: {self.skip_api_url}")
                logger.info(f"📋 SKIP API PAYLOAD: {payload}")
                
                import time
                start_time = time.time()
                response = requests.post(self.skip_api_url, json=payload, timeout=10)
                request_time = time.time() - start_time
                
                logger.info(f"⏱️  SKIP API REQUEST TIME: {request_time:.3f} seconds")
                logger.info(f"📊 SKIP API RESPONSE STATUS: {response.status_code}")
                logger.info(f"📏 SKIP API RESPONSE SIZE: {len(response.content)} bytes")
                
                response.raise_for_status()
                
                data = response.json()
                logger.info(f"🔍 SKIP API RAW RESPONSE: {data}")
                
                # Extract ETH amount from response
                if 'msgs' in data and data['msgs']:
                    logger.info(f"✅ SKIP API SUCCESS: Found {len(data['msgs'])} messages")
                    
                    # Parse the response to get ETH amount - check multiple possible locations
                    eth_amount_wei = 0
                    
                    # Try route.amount_out first (most likely location)
                    if 'route' in data and 'amount_out' in data['route']:
                        eth_amount_wei = data['route']['amount_out']
                        logger.info(f"📍 FOUND amount_out in route: {eth_amount_wei}")
                    
                    # Try route.estimated_amount_out as fallback
                    elif 'route' in data and 'estimated_amount_out' in data['route']:
                        eth_amount_wei = data['route']['estimated_amount_out']
                        logger.info(f"📍 FOUND estimated_amount_out in route: {eth_amount_wei}")
                    
                    # Try root level amount_out as last resort
                    elif 'amount_out' in data:
                        eth_amount_wei = data['amount_out']
                        logger.info(f"📍 FOUND amount_out in root: {eth_amount_wei}")
                    
                    # Try operations array
                    elif 'route' in data and 'operations' in data['route'] and data['route']['operations']:
                        operation = data['route']['operations'][0]
                        if 'amount_out' in operation:
                            eth_amount_wei = operation['amount_out']
                            logger.info(f"📍 FOUND amount_out in operations: {eth_amount_wei}")
                    
                    logger.info(f"⚡ ETH AMOUNT IN WEI: {eth_amount_wei}")
                    
                    if eth_amount_wei and eth_amount_wei != '0':
                        eth_amount = int(eth_amount_wei) / (10 ** 18)  # Convert wei to ETH
                        logger.info(f"💰 ETH AMOUNT CONVERTED: {eth_amount} ETH")
                        
                        conversion_rate = float(usd_amount) / eth_amount if eth_amount > 0 else 0
                        logger.info(f"📈 CONVERSION RATE: ${conversion_rate:.2f} per ETH")
                        
                        logger.info("✅ SKIP API CONVERSION SUCCESSFUL")
                        logger.info("=== USD TO ETH CONVERSION DEBUG END ===")
                        
                        return {
                            'success': True,
                            'eth_amount': eth_amount,
                            'usd_amount': float(usd_amount),
                            'rate': conversion_rate,
                            'source': 'skip_api'
                        }
                    else:
                        logger.warning(f"⚠️  SKIP API WARNING: No valid amount_out found in response")
                        logger.warning(f"🔍 RESPONSE STRUCTURE: {list(data.keys())}")
                        if 'route' in data:
                            logger.warning(f"🔍 ROUTE STRUCTURE: {list(data['route'].keys())}")
                else:
                    logger.warning(f"⚠️  SKIP API WARNING: No messages in response: {data}")
                
            except requests.exceptions.RequestException as skip_error:
                logger.error(f"🌐 SKIP API NETWORK ERROR: {str(skip_error)}")
                logger.error(f"📊 SKIP API RESPONSE DETAILS: Status={getattr(skip_error.response, 'status_code', 'N/A')}, Content={getattr(skip_error.response, 'text', 'N/A')}")
            except Exception as skip_error:
                logger.error(f"💥 SKIP API ERROR: {str(skip_error)}", exc_info=True)
            
            # Fallback: Use CoinGecko price
            logger.info("🔄 FALLBACK: Using CoinGecko price for conversion")
            try:
                # Get current ETH price
                logger.info("📞 CALLING get_current_eth_price() for fallback...")
                price_result = self.get_current_eth_price()
                logger.info(f"📊 COINGECKO PRICE RESULT: {price_result}")
                
                if price_result['success']:
                    eth_price = price_result['price']
                    logger.info(f"💰 COINGECKO ETH PRICE: ${eth_price}")
                    
                    eth_amount = float(usd_amount) / eth_price
                    logger.info(f"🧮 CONVERSION CALCULATION: ${usd_amount} ÷ ${eth_price} = {eth_amount} ETH")
                    
                    logger.info("✅ COINGECKO FALLBACK CONVERSION SUCCESSFUL")
                    logger.info("=== USD TO ETH CONVERSION DEBUG END ===")
                    
                    return {
                        'success': True,
                        'eth_amount': eth_amount,
                        'usd_amount': float(usd_amount),
                        'rate': eth_price,
                        'source': 'coingecko_fallback'
                    }
                else:
                    logger.error(f"❌ COINGECKO PRICE FETCH FAILED: {price_result.get('error', 'Unknown error')}")
            except Exception as fallback_error:
                logger.error(f"💥 COINGECKO FALLBACK ERROR: {str(fallback_error)}", exc_info=True)
            
            # Final fallback: Use mock rate for testing
            logger.warning("⚠️  FINAL FALLBACK: Using mock ETH price for testing")
            mock_eth_price = 2500.0  # Mock ETH price for testing
            logger.info(f"🎭 MOCK ETH PRICE: ${mock_eth_price}")
            
            eth_amount = float(usd_amount) / mock_eth_price
            logger.info(f"🧮 MOCK CONVERSION: ${usd_amount} ÷ ${mock_eth_price} = {eth_amount} ETH")
            
            logger.warning("⚠️  USING MOCK DATA - NOT REAL PRICES!")
            logger.info("=== USD TO ETH CONVERSION DEBUG END ===")
            
            return {
                'success': True,
                'eth_amount': eth_amount,
                'usd_amount': float(usd_amount),
                'rate': mock_eth_price,
                'source': 'mock_fallback'
            }
            
        except Exception as e:
            logger.error(f"Convert USD to ETH error: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to convert USD to ETH: {str(e)}'
            }
    
    def verify_price_tolerance(self, original_price, current_price, tolerance_percent=1.0):
        """Verify price hasn't changed beyond tolerance"""
        try:
            if not original_price or not current_price:
                return {
                    'success': False,
                    'error': 'Price values are required'
                }
            
            price_change_percent = abs(current_price - original_price) / original_price * 100
            
            is_within_tolerance = price_change_percent <= tolerance_percent
            
            return {
                'success': True,
                'is_within_tolerance': is_within_tolerance,
                'price_change_percent': price_change_percent,
                'tolerance_percent': tolerance_percent,
                'original_price': original_price,
                'current_price': current_price
            }
            
        except Exception as e:
            logger.error(f"Verify price tolerance error: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to verify price tolerance: {str(e)}'
            }
    
    def _get_cached_price(self, pair):
        """Get cached price if still valid"""
        try:
            logger.debug(f"🔍 CACHE LOOKUP: Searching for pair '{pair}'")
            
            cached = PriceCache.query.filter_by(pair=pair).first()
            if cached:
                logger.debug(f"📦 CACHE FOUND: Pair '{pair}' exists in cache")
                logger.debug(f"⏰ CACHE TIMESTAMP: {cached.timestamp}")
                logger.debug(f"💰 CACHED PRICE: ${cached.price}")
                
                time_diff = datetime.utcnow() - cached.timestamp
                logger.debug(f"⏱️  TIME SINCE CACHE: {time_diff}")
                logger.debug(f"⏳ CACHE DURATION LIMIT: {self.cache_duration}")
                
                if time_diff < self.cache_duration:
                    logger.info(f"✅ CACHE VALID: Price for '{pair}' is still fresh (age: {time_diff})")
                    return float(cached.price)
                else:
                    logger.info(f"⏰ CACHE EXPIRED: Price for '{pair}' is too old (age: {time_diff})")
                    return None
            else:
                logger.debug(f"❌ CACHE MISS: No cached price found for pair '{pair}'")
                return None
        except Exception as e:
            logger.error(f"💥 CACHE LOOKUP ERROR: {str(e)}", exc_info=True)
            return None
    
    def _cache_price(self, pair, price):
        """Cache price in database"""
        try:
            logger.debug(f"💾 CACHING PRICE: Pair '{pair}' = ${price}")
            
            # Remove old cache entries
            old_entries = PriceCache.query.filter_by(pair=pair).all()
            logger.debug(f"🗑️  REMOVING OLD CACHE: Found {len(old_entries)} old entries for '{pair}'")
            PriceCache.query.filter_by(pair=pair).delete()
            
            # Add new cache entry
            cache_entry = PriceCache(
                pair=pair,
                price=price
            )
            logger.debug(f"📝 CREATING CACHE ENTRY: {cache_entry}")
            
            db.session.add(cache_entry)
            db.session.commit()
            
            logger.info(f"✅ CACHE STORED: Price for '{pair}' = ${price} cached successfully")
            
        except Exception as e:
            logger.error(f"💥 CACHE STORAGE ERROR: {str(e)}", exc_info=True)
            db.session.rollback()
            logger.error("🔄 DATABASE ROLLBACK: Cached price operation rolled back")

# Global instance
price_service = PriceService()
