import collections


class InventoryAllocator:
    def __init__(self):
        pass

    def process_order(self, order, warehouses):
        # Type checking and making sure that the inputs actually have values
        if not isinstance(order, dict) or not isinstance(warehouses, list):
            return []
        if not order or not warehouses:
            return []
        
        output = collections.OrderedDict()
        for item in sorted(order.keys()): # sorting to ensure that each item is looked at in a certain order
            for warehouse in warehouses: # search each warehouse (already "pre-sorted")
                payment = self.check_warehouse(order, warehouse, item)
                # if something is taken from said warehouse, store its name, what was taken, and how much
                if payment > 0:
                    if warehouse["name"] not in output:
                        output[warehouse["name"]] = {}
                    output[warehouse["name"]][item] = payment
                if order[item] == 0: # if item request is fulfilled, move on to the next
                    break
            if order[item] != 0: # if one item can't be fuilfilled, the whole order can't be completed 
                return []

        return [{k: v} for k, v in output.items()] # transform the output dict into a list

    def check_warehouse(self, order, warehouse, item):
        amount_taken = 0
        if item in warehouse["inventory"]:
            # if the item exists within the warehouse take the minimum of what's needed and the amount
            # of stock that the warehouse has
            amount_taken = min(order[item], warehouse["inventory"][item])
            order[item] -= amount_taken
            warehouse["inventory"][item] -= amount_taken
        return amount_taken