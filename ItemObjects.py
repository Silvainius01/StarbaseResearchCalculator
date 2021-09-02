

class MaterialItem:
    def __init__(self, matName: str, baseWeight: float):
        self.name = matName
        self.researchWeight = baseWeight
        self.materialPairWeights = {}
        self.price = -1
        pass
    def AddMaterialPairWeight(self, material: str, pairWeight: float):
        self.materialPairWeights[material] = pairWeight
        pass
    def UpdatePrice(self, price: int):
        self.price = price
    def GetKvCreditCost(self, numKv: float):
        return (numKv / 1728.0) * self.price
    pass

materials = {
            "aegisium": MaterialItem("aegsium", 2),
            "ajatite": MaterialItem("ajatite", 0.5),
            "arkanium": MaterialItem("arkanium", 100),
            "bastium": MaterialItem("bastium", 1),
            "charodium": MaterialItem("charodium", 1),
            "corazium": MaterialItem("corazium", 100),
            "daltium": MaterialItem("daltium", 100),
            "exorium": MaterialItem("aegexoriumium", 2),
            "haderite": MaterialItem("haderite", 100),
            "ice": MaterialItem("ice", 0.5),
            "ilmatrium": MaterialItem("ilmatrium", 100),
            "karnite": MaterialItem("karnite", 100),
            "kutonium": MaterialItem("kutonium", 100),
            "lukium": MaterialItem("lukium", 100),
            "merkerium": MaterialItem("merkerium", 100),
            "naflite": MaterialItem("naflite", 100),
            "nhurgite": MaterialItem("nhurgite", 1.5),
            "oninum": MaterialItem("oninum", 100),
            "surtrite": MaterialItem("surtrite", 100),
            "targium": MaterialItem("targium", 100),
            "tengium": MaterialItem("tengium", 100),
            "ukonium": MaterialItem("ukonium", 100),
            "valkite": MaterialItem("valkite", 0.5),
            "vokarium": MaterialItem("vokarium", 1),
            "xhallium": MaterialItem("xhallium", 100),
            "ymrium": MaterialItem("ymrium", 100)
        }
research = {
    "red": 0,
    "yellow": 0,
    "purple": 0,
    "blue": 0,
}

def __create_material_pair__(matOne: str, matTwo: str, weight: float):
    materials[matOne].AddMaterialPairWeight(matTwo, weight)
    materials[matTwo].AddMaterialPairWeight(matOne, weight)
    pass

def init_material_pairs():
    # z1 Valkite
    __create_material_pair__("valkite", "bastium", 0.5)
    __create_material_pair__("valkite", "vokarium", 1)  # dont affect value (reported, never found)
    # z2 Valkite
    __create_material_pair__("valkite", "aegisium", 0.8)
    __create_material_pair__("valkite", "vokarium", 1)  # dont affect the value
    __create_material_pair__("valkite", "exorium", 0.8)
    # z5 Valkite
    __create_material_pair__("valkite", "charodium", 1)  # dont affect the value
    __create_material_pair__("valkite", "karnite", 1)  # dont affect the value
    __create_material_pair__("valkite", "corazium", 0.75)

    # z1 Ice
    __create_material_pair__("ice", "vokarium", 0.5)
    __create_material_pair__("ice", "nhurgite", 0.8)
    # z3 Ice
    __create_material_pair__("ice", "arkanium", 0.8)
    __create_material_pair__("ice", "aegisium", 1)  # dont affect value

    # z1 Ajatite
    __create_material_pair__("ajatite", "charodium", 0.5)
    __create_material_pair__("ajatite", "nhurgite", 1)  # dont affect value (reported, never found)
    # z2 Ajatite
    __create_material_pair__("ajatite", "vokarium", 0.8)
    __create_material_pair__("ajatite", "nhurgite", 0.9)
    # z4 Ajatite
    __create_material_pair__("ajatite", "karnite", 0.8)
    __create_material_pair__("ajatite", "aegisium", 1)  # dont affect value
    pass

def estimate_crafting_time(materialCost: dict):
    return sum(materialCost.values()) / 100.0

class ResearchMaterialRate:
    def __init__(self, matName, researchValue: int, materialCost: dict):
        numKv = materialCost.get(matName, 0)
        rate = numKv / researchValue if researchValue > 0 else 0
        material = materials[matName]

        self.rawRate = rate if rate > 0 else 0
        self.materialRate = rate * material.researchWeight
        self.manualRate = rate * material.researchWeight
        self.creditRate = material.GetKvCreditCost(numKv) / researchValue if researchValue > 0 else -1

        # multiply successive material weights
        for mk, mv in material.materialPairWeights.items():
            if mk in materialCost:
                self.manualRate *= mv

        pass

    def AddRate(self, otherRate):
        self.rawRate += otherRate.rawRate
        self.materialRate += otherRate.materialRate
        self.manualRate += otherRate.manualRate
        self.creditRate += otherRate.creditRate
        pass
    pass
class ResearchRate(dict):
    def __init__(self, researchValue: int, craftTime: float, materialCost: dict):
        self.timeRate = researchValue / craftTime if craftTime > 0 else 0
        self.materialRates = {}
        self.totalRate = ResearchMaterialRate("ice", 0, {})
        pass

    def AddRate(self, matName: str, matResearchRate: ResearchMaterialRate):
        self.materialRates[matName] = matResearchRate
        self.totalRate.AddRate(matResearchRate)
        pass

    def as_export(self):
        exportDict = {
            "timeRate": self.timeRate,
            "totalRates": self.totalRate.__dict__,
            "materialRates": {k:v.__dict__ for k,v in self.materialRates.items()}
        }
        return exportDict
    pass


class CraftItem:
    def __init__(self, name: str, researchValue: dict, materialCost: dict, craftTime: float):
        if craftTime <= 0:
            craftTime = estimate_crafting_time(materialCost)

        self.name = name
        self.researchValue = researchValue
        self.materialCost = materialCost
        self.craftTime = craftTime

        self.researchRates = {}
        self.totalResearchRate = ResearchRate(sum(researchValue.values()), craftTime, materialCost)
        for k in research.keys():
            self.researchRates[k] = ResearchRate(researchValue.get(k, 0), craftTime, materialCost)

        self.__calculate_material_rate__()
        pass

    def __calculate_material_rate__(self):
        for rk, rv in self.researchValue.items():
            for mk, mv in self.materialCost.items():
                rate = ResearchMaterialRate(mk, rv, self.materialCost)
                self.researchRates[rk].AddRate(mk, rate)
        pass

    def as_export(self):
        exportDict = {
            "name": self.name,
            "craftTime": self.craftTime,
            "materialCost": self.materialCost,
            "researchValue": self.researchValue,
            "researchRates": {k:{} for k in self.researchValue.keys()}
        }
        for rk in self.researchValue.keys():
            # for mk in self.materialCost.keys():
                exportDict["researchRates"][rk] = self.researchRates[rk].as_export()
            #exportDict["researchRates"][rk]["total"] = self.totalResearchRate[rk].__dict__
        return exportDict
    pass