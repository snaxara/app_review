"""
Modelo de BusinessCapability para estrutura hierárquica de capacidades de negócio
"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel
from datetime import datetime
import uuid


class CapabilityType(str, Enum):
    """Tipo de capacidade de negócio"""
    CORE = "Core"
    SUPPORTING = "Supporting"
    STRATEGIC = "Strategic"


class Maturity(str, Enum):
    """Nível de maturidade da capacidade"""
    INITIAL = "Initial"
    MANAGED = "Managed"
    DEFINED = "Defined"
    OPTIMIZED = "Optimized"


class BusinessValue(str, Enum):
    """Valor de negócio da capacidade"""
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class BusinessCapability(BaseModel):
    """Modelo de BusinessCapability conforme especificação do gestor"""
    
    id: str
    name: str
    description: str
    level: int  # 1-3 (hierarquia)
    parent_id: Optional[str] = None  # Para hierarquia
    capability_type: CapabilityType
    maturity: Maturity
    business_value: BusinessValue
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    
    def __init__(self, **data):
        if 'id' not in data:
            data['id'] = str(uuid.uuid4())
        super().__init__(**data)
    
    class Config:
        use_enum_values = True


# Mapeamento das categorias funcionais para BusinessCapability
CATEGORY_TO_CAPABILITY = {
    "PIX": {
        "name": "Transferências PIX",
        "description": "Capacidade de realizar transferências instantâneas via PIX",
        "level": 2,
        "capability_type": CapabilityType.CORE,
        "maturity": Maturity.MANAGED,
        "business_value": BusinessValue.HIGH
    },
    "Login/Autenticação": {
        "name": "Autenticação e Acesso",
        "description": "Capacidade de autenticação segura e acesso ao aplicativo",
        "level": 1,
        "capability_type": CapabilityType.CORE,
        "maturity": Maturity.MANAGED,
        "business_value": BusinessValue.HIGH
    },
    "Performance": {
        "name": "Performance e Estabilidade",
        "description": "Capacidade de manter performance e estabilidade do aplicativo",
        "level": 1,
        "capability_type": CapabilityType.SUPPORTING,
        "maturity": Maturity.MANAGED,
        "business_value": BusinessValue.HIGH
    },
    "Interface/Usabilidade": {
        "name": "Interface e Experiência do Usuário",
        "description": "Capacidade de fornecer interface intuitiva e usável",
        "level": 1,
        "capability_type": CapabilityType.SUPPORTING,
        "maturity": Maturity.MANAGED,
        "business_value": BusinessValue.MEDIUM
    },
    "Empréstimos/Crédito": {
        "name": "Empréstimos e Crédito",
        "description": "Capacidade de oferecer produtos de crédito e empréstimos",
        "level": 2,
        "capability_type": CapabilityType.CORE,
        "maturity": Maturity.MANAGED,
        "business_value": BusinessValue.HIGH
    },
    "Pagamentos/Boletos": {
        "name": "Pagamentos e Boletos",
        "description": "Capacidade de processar pagamentos e boletos",
        "level": 2,
        "capability_type": CapabilityType.CORE,
        "maturity": Maturity.MANAGED,
        "business_value": BusinessValue.HIGH
    },
    "Saldo/Extrato": {
        "name": "Consulta de Saldo e Extrato",
        "description": "Capacidade de consultar saldo e histórico de transações",
        "level": 2,
        "capability_type": CapabilityType.CORE,
        "maturity": Maturity.MANAGED,
        "business_value": BusinessValue.HIGH
    },
    "Atendimento": {
        "name": "Atendimento ao Cliente",
        "description": "Capacidade de fornecer suporte e atendimento ao cliente",
        "level": 2,
        "capability_type": CapabilityType.SUPPORTING,
        "maturity": Maturity.MANAGED,
        "business_value": BusinessValue.MEDIUM
    },
    "Cadastro/Conta": {
        "name": "Gestão de Cadastro e Conta",
        "description": "Capacidade de gerenciar cadastro e dados da conta",
        "level": 2,
        "capability_type": CapabilityType.SUPPORTING,
        "maturity": Maturity.MANAGED,
        "business_value": BusinessValue.MEDIUM
    },
    "Investimentos": {
        "name": "Investimentos",
        "description": "Capacidade de oferecer produtos de investimento",
        "level": 2,
        "capability_type": CapabilityType.STRATEGIC,
        "maturity": Maturity.MANAGED,
        "business_value": BusinessValue.HIGH
    },
    "Segurança": {
        "name": "Segurança e Proteção",
        "description": "Capacidade de garantir segurança e proteção dos dados",
        "level": 1,
        "capability_type": CapabilityType.CORE,
        "maturity": Maturity.MANAGED,
        "business_value": BusinessValue.HIGH
    },
    "Notificações": {
        "name": "Notificações e Alertas",
        "description": "Capacidade de enviar notificações e alertas aos usuários",
        "level": 2,
        "capability_type": CapabilityType.SUPPORTING,
        "maturity": Maturity.MANAGED,
        "business_value": BusinessValue.MEDIUM
    },
    "Questões geográficas": {
        "name": "Acesso Geográfico",
        "description": "Capacidade de acesso em diferentes localizações geográficas",
        "level": 2,
        "capability_type": CapabilityType.SUPPORTING,
        "maturity": Maturity.INITIAL,
        "business_value": BusinessValue.LOW
    },
    "Tarifas/Cobranças": {
        "name": "Gestão de Tarifas",
        "description": "Capacidade de gerenciar tarifas e cobranças",
        "level": 2,
        "capability_type": CapabilityType.SUPPORTING,
        "maturity": Maturity.MANAGED,
        "business_value": BusinessValue.MEDIUM
    },
    "Outros": {
        "name": "Outras Funcionalidades",
        "description": "Outras funcionalidades não categorizadas",
        "level": 3,
        "capability_type": CapabilityType.SUPPORTING,
        "maturity": Maturity.INITIAL,
        "business_value": BusinessValue.LOW
    }
}
