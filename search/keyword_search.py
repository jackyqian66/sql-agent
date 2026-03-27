class KeywordSearch:
    def __init__(self, documents=None):
        self.documents = documents or []

    def search(self, query, k=5):
        try:
            results = []
            for i, doc in enumerate(self.documents):
                content = doc.text or ''
                score = self.calculate_relevance(content, query)
                if score > 0:
                    results.append({"text": doc.text, "score": score, "index": i})
            
            results.sort(key=lambda x: x["score"], reverse=True)
            return {"success": True, "results": results[:k]}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def calculate_relevance(self, content, query):
        query_terms = query.lower().split()
        content_lower = content.lower()
        score = 0
        
        for term in query_terms:
            if term in content_lower:
                score += 1
        
        return score
