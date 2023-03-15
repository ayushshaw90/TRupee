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

    @sp.entry_point
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
        data_to_be_send = sp.record(
            from_ = sp.sender,
            to_ = sp.self_address,
            value = params.amount
        )
        sp.transfer(data_to_be_send, sp.mutez(0), c)
        self.data.escrows[self.data.escrow_id] = sp.record(
            owner = sp.sender,
            token_address = params.token_address,
            token_id = params.token_id,
            amount = params.amount,
            price = params.price
        )
        self.data.escrow_id += 1

    @sp.entry_point
    def exchange(self, params):
        sp.set_type(
            params, sp.TNat
        )
        sp.verify(self.data.escrows.contains(params), "Escrow ID unavailable")
        sp.verify(self.data.escrows[params].price == sp.amount)
        data_type = sp.TRecord(
            from_ = sp.TAddress,
            to_ = sp.TAddress,
            value = sp.TNat
        ).layout(("from_ as from", ("to_ as to", "value")))
        c=sp.contract(data_type, self.data.escrows[params].token_address, "transfer").open_some()
        data_to_be_sent = sp.record(
            from_ = sp.self_address,
            to_ = sp.sender,
            value = self.data.escrows[params].amount
        )
        sp.send(self.data.escrows[params].owner, sp.amount)
        sp.transfer(data_to_be_sent, sp.mutez(0), c)
        del self.data.escrows[params]

if "templates" not in __name__:
    @sp.add_test(name="Contract creation")
    def test():
        scenario = sp.test_scenario()
        c1 = Escrow()
        scenario+=c1
    
    
            