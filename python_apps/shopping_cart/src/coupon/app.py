import json
import random

def lambda_handler(event, context):
    
    coupon_name = ""
    coupon_discount_pct = 0
    
    #get a random number between 1 and 3
    random_number = random.randint(1, 3)
    
    if random_number == 1:
        coupon_name = "10% off your item"
        coupon_discount_pct = 10
    elif random_number == 2:
        coupon_name = "20% off your item"
        coupon_discount_pct = 20
    elif random_number == 3:
        coupon_name = "30% off your item"
        coupon_discount_pct = 30
        
    return {
        "statusCode": 200,
        "body": json.dumps({
            "couponName": coupon_name,
            "couponDiscountPct": coupon_discount_pct
        })
    }