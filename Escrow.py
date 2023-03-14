import smartpy as sp

class Escrow(sp.Contract):
    def __init__(self):
        self.init(
            escrow_id = sp.nat(0),
            escrows = sp.big_map(
                tkey = sp.TNat,
                tvalue = sp.TRecord(
                    owner = sp.TAddress,
                    token_address = sp.TAddress,
                    token_id = sp.TNat,
                    amount = sp.TNat,
                    price = sp.TMutez
                )
            )
        )

    def create_escrow(self, params):
        sp.set_type(
            params, sp.TRecord(
                price = sp.TMutez,
                token_id = sp.TNat,
                token_address = sp.TAddress,
                amount = sp.TNat
            )
        )
        data_type = sp.TRecord(
            from_ = sp.TAddress,
            to_ = sp.TAddress,
            value = sp.TNat
        ).layout(("from_ as from", ("to_ as to", "value")))
        c = sp.contract(data_type, params.token_address, "transfer").open_some()
        data_to_be_send = sp.TRecord(
            from_ = sp.sender,
            to_ = sp.self_address,
            value = params.amount
        )
        sp.transfer(data_to_be_send, sp.mutez(0), c)
        sp.data.escrows[self.data.escrow_id] = sp.record(
            owner = sp.sender,
            token_address = params.token_address,
            token_id = params.token_id,
            amount = params.amount,
            price = params.price
        )
        self.data.escrow_id += 1
        