"""
MCP Server (Model Context Protocol) pour le système médical
"""

import json
import asyncio
from typing import Dict, Any, List
from datetime import datetime
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MCPServer:
    """Serveur MCP qui fournit des contextes et outils médicaux"""
    
    def __init__(self, data_path: str = "data"):
        self.data_path = Path(__file__).parent / data_path
        self.data_path.mkdir(exist_ok=True)
        self.medical_db_path = self.data_path / "medical_db.json"
        self.initialize_database()
        
    def initialize_database(self):
        """Initialise la base de données médicale"""
        if not self.medical_db_path.exists():
            initial_data = {
                "symptom_database": {
                    "respiratory": {
                        "keywords": ["toux", "fièvre", "respiration", "essoufflement", "gorge", "nez"],
                        "common_conditions": ["infection respiratoire", "bronchite", "rhume"],
                        "red_flags": ["difficulté respiratoire", "douleur thoracique"],
                        "advice": "Repos, hydratation, éviter le tabac"
                    },
                    "digestive": {
                        "keywords": ["nausée", "vomissement", "diarrhée", "douleur abdominale"],
                        "common_conditions": ["gastro-entérite", "intoxication alimentaire"],
                        "red_flags": ["sang dans selles", "déshydratation sévère"],
                        "advice": "Régime léger, réhydratation orale"
                    },
                    "neurological": {
                        "keywords": ["maux tête", "vertige", "confusion", "vision"],
                        "common_conditions": ["migraine", "céphalée"],
                        "red_flags": ["paralysie", "perte conscience"],
                        "advice": "Repos au calme, éviter écrans"
                    }
                },
                "consultations_history": []
            }
            self.save_json(self.medical_db_path, initial_data)
    
    def save_json(self, path: Path, data: Any):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def load_json(self, path: Path) -> Any:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    async def analyze_symptoms_tool(self, symptoms: str) -> Dict[str, Any]:
        """Analyse les symptômes et retourne des suggestions"""
        logger.info(f"Analyzing symptoms: {symptoms}")
        db = self.load_json(self.medical_db_path)
        
        for category, data in db["symptom_database"].items():
            for keyword in data["keywords"]:
                if keyword in symptoms.lower():
                    return {
                        "category": category,
                        "possible_conditions": data["common_conditions"][:2],
                        "red_flags": data["red_flags"],
                        "advice": data["advice"],
                        "confidence": 0.7
                    }
        
        return {
            "category": "general",
            "possible_conditions": ["consultation médicale recommandée"],
            "red_flags": [],
            "advice": "Consultez un médecin pour évaluation",
            "confidence": 0.3
        }
    
    async def save_consultation_tool(self, consultation_data: Dict) -> Dict:
        """Sauvegarde une consultation dans l'historique"""
        db = self.load_json(self.medical_db_path)
        
        record = {
            "id": len(db["consultations_history"]) + 1,
            "timestamp": datetime.now().isoformat(),
            "data": consultation_data
        }
        
        db["consultations_history"].append(record)
        self.save_json(self.medical_db_path, db)
        
        return {"status": "saved", "id": record["id"]}
    
    async def get_consultation_history_tool(self, limit: int = 10) -> List[Dict]:
        """Récupère l'historique des consultations"""
        db = self.load_json(self.medical_db_path)
        return db["consultations_history"][-limit:]

class MCPClient:
    """Client pour interagir avec MCP depuis LangGraph"""
    
    def __init__(self):
        self.server = MCPServer()
    
    async def analyze_symptoms(self, symptoms: str) -> Dict:
        return await self.server.analyze_symptoms_tool(symptoms)
    
    async def save_consultation(self, data: Dict) -> Dict:
        return await self.server.save_consultation_tool(data)
    
    async def get_history(self, limit: int = 10) -> List[Dict]:
        return await self.server.get_consultation_history_tool(limit)

if __name__ == "__main__":
    async def test():
        client = MCPClient()
        result = await client.analyze_symptoms("fièvre et toux")
        print("Test MCP Server:", result)
    
    asyncio.run(test())