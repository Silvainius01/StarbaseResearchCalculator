import json
from ItemObjects import *

def default_research_item_dict():
    return {
        "red": CraftItem("YOU SHOULD NOT SEE THIS", {}, {}, -1),
        "blue": CraftItem("YOU SHOULD NOT SEE THIS", {}, {}, -1),
        "yellow": CraftItem("YOU SHOULD NOT SEE THIS", {}, {}, -1),
        "purple": CraftItem("YOU SHOULD NOT SEE THIS", {}, {}, -1)
    }

class CraftingResearchAnalyzer:
    def __init__(self):
        self.craft_items = {}
        self.best_item_kvs_manual = default_research_item_dict() # best items when manually mining mates
        self.best_item_kvs_material = default_research_item_dict() # best items based on mats, not accounting for material pairs
        self.best_item_kvs_raw = default_research_item_dict() # best items based on raw kv requirements, with no multipliers.
        pass

    def update_best_items(self, item: CraftItem):
        for rColor in research.keys():
            itemRates = item.researchRates[rColor].totalRate

            # raw
            bestRates = self.best_item_kvs_raw[rColor].researchRates[rColor].totalRate
            if bestRates.rawRate <= 0 or itemRates.rawRate < bestRates.rawRate:
                self.best_item_kvs_raw[rColor] = item

            # material
            bestRates = self.best_item_kvs_material[rColor].researchRates[rColor].totalRate
            if bestRates.materialRate <= 0 or itemRates.materialRate < bestRates.materialRate:
                self.best_item_kvs_material[rColor] = item

            # manual
            bestRates = self.best_item_kvs_manual[rColor].researchRates[rColor].totalRate
            if bestRates.manualRate <= 0 or itemRates.manualRate < bestRates.manualRate:
                self.best_item_kvs_manual[rColor] = item
        pass

    def import_data_from_json(self, path: str):
        with open(path) as file:
            self.import_raw_data(json.load(file))
        pass

    def import_raw_data(self, test_data: dict):
        for itemName, itemData in test_data.items():
            item = CraftItem(
                itemName,
                {k: v for k, v in itemData.items() if k in research},
                {k: v for k, v in itemData.items() if k in materials},
                test_data.get("time", 0)
            )
            self.craft_items[item.name] = item
            self.update_best_items(item)
        debugLmao = True
        pass

    def export_data_raw(self, path):
        """Exports data in the form that the analyzer received it"""
        with open(path, 'w') as file:
            exportDict = {}
            for k,v in self.craft_items.items():
                exportItem = {}
                for mk, mv in v.materialCost.items():
                    exportItem[mk] = mv
                for rk, rv in v.researchValue.items():
                    exportItem[rk] = rv
                exportDict[k] = exportItem
                pass
            json.dump(exportDict, file)
        pass

    def export_data(self, path):
        """Export all processed research data"""
        with open(path, 'w') as file:
            exportDict = {
                "BestItemsRaw": self.filter_best_export_dict(self.best_item_kvs_raw),
                "BestItemsMaterial": self.filter_best_export_dict(self.best_item_kvs_material),
                "BestItemsManual": self.filter_best_export_dict(self.best_item_kvs_manual),
                "ItemData": {}
            }
            for k,v in self.craft_items.items():
                exportDict["ItemData"][v.name] = v.as_export()
            json.dump(exportDict, file)
        pass
    def filter_best_export_dict(self, dict: dict):
        exportDict = {}
        for rk, rv in dict.items():
            if rk in rv.researchValue:
                exportDict[rk] = rv.as_export()
        return exportDict
    pass