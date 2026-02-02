from . import model

dallas_terminal_e_bagdrop = model.Location.model_validate({
    'lat': 32.88905,
    'lon': -97.03634,
    'description': 'DFW Terminal E Bag Drop',
    'code': 'dfw'
})

dallas_terminal_e_aboard_aircraft = model.Location.model_validate({
    'lat': 32.89170,
    'lon': -97.03527,
    'description': 'Aboard UA1564',
    'code': 'dfw'
})

chicago_terminal_1_gate = model.Location.model_validate({
    'lat': 41.97885,
    'lon': -87.90745,
    'description': 'At United gate - Chicago Terminal 1',
    'code': 'ord'
})

chicago_bag_claim_1 = model.Location.model_validate({
    'lat': 41.97998,
    'lon': -87.90609,
    'description': 'Chicago Terminal 1 Bag Claim 1',
    'code': 'ord'
})


boston_terminal_b_aboard_aircraft = model.Location.model_validate({
    'lat': 41.97885,
    'lon': -87.90745,
    'description': 'At United gate - Boston Logan Terminal B',
    'code': 'bos'

})

boston_bag_claim_1 = model.Location.model_validate({
    'lat': 42.36215,
    'lon': -71.01778,
    'description': 'Boston Logan Terminal B Bag Claim 4',
    'code': 'bos'
    
})

corrupt_data=0b011001000110010101100101011100000100100101101110010101000110100001100101010010000110010101100001011100100111010001001111011001100101010001100101011110000110000101110011
