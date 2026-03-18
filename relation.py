class RelationNode:
    def __init__(self, id, word1, word2, relation_typeid, relation_typename):
        self.id = id
        self.word1 = word1
        self.word2 = word2
        self.relation_typeid = relation_typeid
        self.relation_typename = relation_typename
        self.annotation_score = 0
        

    def __repr__(self):
        return f"{self.word1} {self.relation_typename} {self.word2}"

class CoupleRelation:
    def __init__(self, relation1, relation2):
        if isinstance(relation1, RelationNode) and isinstance(relation2, RelationNode):
            self.relation1 = relation1
            self.relation2 = relation2
            self.pertinence_score = (relation1.annotation_score+relation2.annotation_score)/2
        else:
            print("Erreur : les deux arguments doivent être des instances de RelationNode.")

    def __repr__(self):
        return f"{self.relation1} & {self.relation2}"
