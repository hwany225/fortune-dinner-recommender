# -*- coding: utf-8 -*-
"""
JSON 스키마 검증 로직
API 요청 및 응답 데이터의 유효성을 검증하는 스키마 정의
"""

from typing import Dict, Any, List
import jsonschema
from jsonschema import validate, ValidationError
from datetime import datetime


class ValidationSchemas:
    """JSON 스키마 정의 클래스"""
    
    # 개인 운세 요청 스키마
    INDIVIDUAL_FORTUNE_REQUEST = {
        "type": "object",
        "properties": {
            "mode": {
                "type": "string",
                "enum": ["individual"]
            },
            "participants": {
                "type": "array",
                "minItems": 1,
                "maxItems": 1,
                "items": {
                    "type": "object",
                    "properties": {
                        "birth_date": {
                            "type": "string",
                            "pattern": r"^\d{4}-\d{2}-\d{2}$"
                        },
                        "name": {
                            "type": "string",
                            "minLength": 1,
                            "maxLength": 50
                        }
                    },
                    "required": ["birth_date"],
                    "additionalProperties": False
                }
            }
        },
        "required": ["mode", "participants"],
        "additionalProperties": False
    }
    
    # 그룹 운세 요청 스키마
    GROUP_FORTUNE_REQUEST = {
        "type": "object",
        "properties": {
            "mode": {
                "type": "string",
                "enum": ["group"]
            },
            "participants": {
                "type": "array",
                "minItems": 2,
                "maxItems": 10,
                "items": {
                    "type": "object",
                    "properties": {
                        "birth_date": {
                            "type": "string",
                            "pattern": r"^\d{4}-\d{2}-\d{2}$"
                        },
                        "name": {
                            "type": "string",
                            "minLength": 1,
                            "maxLength": 50
                        }
                    },
                    "required": ["birth_date"],
                    "additionalProperties": False
                }
            }
        },
        "required": ["mode", "participants"],
        "additionalProperties": False
    }
    
    # 카테고리 운세 스키마
    CATEGORY_FORTUNE_SCHEMA = {
        "type": "object",
        "properties": {
            "score": {
                "type": "integer",
                "minimum": 1,
                "maximum": 100
            },
            "message": {
                "type": "string",
                "minLength": 1
            },
            "keywords": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            }
        },
        "required": ["score", "message"],
        "additionalProperties": False
    }
    
    # 개인 운세 응답 스키마
    INDIVIDUAL_FORTUNE_RESPONSE = {
        "type": "object",
        "properties": {
            "date": {
                "type": "string",
                "pattern": r"^\d{4}-\d{2}-\d{2}$"
            },
            "mode": {
                "type": "string",
                "enum": ["individual"]
            },
            "fortune": {
                "type": "object",
                "properties": {
                    "love": {"$ref": "#/definitions/category_fortune"},
                    "health": {"$ref": "#/definitions/category_fortune"},
                    "wealth": {"$ref": "#/definitions/category_fortune"},
                    "career": {"$ref": "#/definitions/category_fortune"}
                },
                "required": ["love", "health", "wealth", "career"],
                "additionalProperties": False
            },
            "total_score": {
                "type": "integer",
                "minimum": 1,
                "maximum": 100
            }
        },
        "required": ["date", "mode", "fortune", "total_score"],
        "additionalProperties": False,
        "definitions": {
            "category_fortune": CATEGORY_FORTUNE_SCHEMA
        }
    }
    
    # 그룹 운세 응답 스키마
    GROUP_FORTUNE_RESPONSE = {
        "type": "object",
        "properties": {
            "date": {
                "type": "string",
                "pattern": r"^\d{4}-\d{2}-\d{2}$"
            },
            "mode": {
                "type": "string",
                "enum": ["group"]
            },
            "individual_fortunes": {
                "type": "array",
                "minItems": 2,
                "maxItems": 10,
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string"
                        },
                        "fortune": {
                            "type": "object",
                            "properties": {
                                "love": {"$ref": "#/definitions/category_fortune"},
                                "health": {"$ref": "#/definitions/category_fortune"},
                                "wealth": {"$ref": "#/definitions/category_fortune"},
                                "career": {"$ref": "#/definitions/category_fortune"}
                            },
                            "required": ["love", "health", "wealth", "career"],
                            "additionalProperties": False
                        },
                        "total_score": {
                            "type": "integer",
                            "minimum": 1,
                            "maximum": 100
                        }
                    },
                    "required": ["fortune", "total_score"],
                    "additionalProperties": False
                }
            },
            "group_fortune": {
                "type": "object",
                "properties": {
                    "average_score": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 100
                    },
                    "harmony_score": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 100
                    },
                    "dominant_categories": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "enum": ["love", "health", "wealth", "career"]
                        }
                    },
                    "group_message": {
                        "type": "string",
                        "minLength": 1
                    }
                },
                "required": ["average_score", "harmony_score", "dominant_categories", "group_message"],
                "additionalProperties": False
            }
        },
        "required": ["date", "mode", "individual_fortunes", "group_fortune"],
        "additionalProperties": False,
        "definitions": {
            "category_fortune": CATEGORY_FORTUNE_SCHEMA
        }
    }
    
    # 메뉴 추천 요청 스키마
    MENU_RECOMMENDATION_REQUEST = {
        "type": "object",
        "properties": {
            "mode": {
                "type": "string",
                "enum": ["individual", "group"]
            },
            "fortune_data": {
                "type": "object",
                "properties": {
                    "individual_score": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 100
                    },
                    "group_score": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 100
                    },
                    "harmony_score": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 100
                    },
                    "participant_count": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 10
                    },
                    "dominant_categories": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "enum": ["love", "health", "wealth", "career"]
                        }
                    },
                    "keywords": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    }
                },
                "additionalProperties": False
            }
        },
        "required": ["mode", "fortune_data"],
        "additionalProperties": False
    }
    
    # 메뉴 추천 응답 스키마
    MENU_RECOMMENDATION_RESPONSE = {
        "type": "object",
        "properties": {
            "recommendations": {
                "type": "array",
                "minItems": 1,
                "maxItems": 3,
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {
                            "type": "string"
                        },
                        "name": {
                            "type": "string"
                        },
                        "reason": {
                            "type": "string"
                        },
                        "ingredients": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        },
                        "cooking_time": {
                            "type": "string"
                        },
                        "difficulty": {
                            "type": "string",
                            "enum": ["쉬움", "보통", "어려움"]
                        },
                        "serving_size": {
                            "type": "string"
                        },
                        "category": {
                            "type": "string",
                            "enum": ["한식", "중식", "일식", "양식", "기타"]
                        },
                        "description": {
                            "type": "string"
                        },
                        "group_benefit": {
                            "type": "string"
                        }
                    },
                    "required": ["id", "name", "reason", "ingredients", "cooking_time", "difficulty", "category"],
                    "additionalProperties": False
                }
            }
        },
        "required": ["recommendations"],
        "additionalProperties": False
    }


class DataValidator:
    """데이터 검증 클래스"""
    
    @staticmethod
    def validate_fortune_request(data: Dict[str, Any]) -> None:
        """운세 요청 데이터 검증"""
        mode = data.get("mode")
        
        if mode == "individual":
            schema = ValidationSchemas.INDIVIDUAL_FORTUNE_REQUEST
        elif mode == "group":
            schema = ValidationSchemas.GROUP_FORTUNE_REQUEST
        else:
            raise ValidationError("mode는 'individual' 또는 'group'이어야 합니다")
        
        validate(instance=data, schema=schema)
        
        # 추가 날짜 검증
        DataValidator._validate_birth_dates(data["participants"])
    
    @staticmethod
    def validate_fortune_response(data: Dict[str, Any]) -> None:
        """운세 응답 데이터 검증"""
        mode = data.get("mode")
        
        if mode == "individual":
            schema = ValidationSchemas.INDIVIDUAL_FORTUNE_RESPONSE
        elif mode == "group":
            schema = ValidationSchemas.GROUP_FORTUNE_RESPONSE
        else:
            raise ValidationError("mode는 'individual' 또는 'group'이어야 합니다")
        
        validate(instance=data, schema=schema)
    
    @staticmethod
    def validate_menu_request(data: Dict[str, Any]) -> None:
        """메뉴 추천 요청 데이터 검증"""
        validate(instance=data, schema=ValidationSchemas.MENU_RECOMMENDATION_REQUEST)
    
    @staticmethod
    def validate_menu_response(data: Dict[str, Any]) -> None:
        """메뉴 추천 응답 데이터 검증"""
        validate(instance=data, schema=ValidationSchemas.MENU_RECOMMENDATION_RESPONSE)
    
    @staticmethod
    def _validate_birth_dates(participants: List[Dict[str, Any]]) -> None:
        """생년월일 유효성 검증"""
        current_date = datetime.now().date()
        
        for participant in participants:
            birth_date_str = participant["birth_date"]
            try:
                birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date()
                
                # 미래 날짜 검증
                if birth_date > current_date:
                    raise ValidationError(f"생년월일은 미래 날짜일 수 없습니다: {birth_date_str}")
                
                # 너무 오래된 날짜 검증 (1900년 이후)
                if birth_date.year < 1900:
                    raise ValidationError(f"생년월일이 너무 오래되었습니다: {birth_date_str}")
                
                # 너무 최근 날짜 검증 (최소 1세 이상)
                min_age_date = datetime(current_date.year - 1, current_date.month, current_date.day).date()
                if birth_date > min_age_date:
                    raise ValidationError(f"최소 1세 이상이어야 합니다: {birth_date_str}")
                    
            except ValueError as e:
                if "does not match format" in str(e):
                    raise ValidationError(f"잘못된 날짜 형식입니다: {birth_date_str}")
                raise ValidationError(f"유효하지 않은 날짜입니다: {birth_date_str}")


def validate_json_data(data: Dict[str, Any], validation_type: str) -> None:
    """
    JSON 데이터 검증 통합 함수
    
    Args:
        data: 검증할 데이터
        validation_type: 검증 타입 ('fortune_request', 'fortune_response', 'menu_request', 'menu_response')
    
    Raises:
        ValidationError: 검증 실패 시
    """
    validator = DataValidator()
    
    try:
        if validation_type == "fortune_request":
            validator.validate_fortune_request(data)
        elif validation_type == "fortune_response":
            validator.validate_fortune_response(data)
        elif validation_type == "menu_request":
            validator.validate_menu_request(data)
        elif validation_type == "menu_response":
            validator.validate_menu_response(data)
        else:
            raise ValueError(f"지원하지 않는 검증 타입입니다: {validation_type}")
            
    except ValidationError as e:
        # 한국어 오류 메시지로 변환
        error_msg = str(e)
        if "is not valid under any of the given schemas" in error_msg:
            error_msg = "제공된 데이터가 유효한 스키마와 일치하지 않습니다"
        elif "is a required property" in error_msg:
            missing_field = error_msg.split("'")[1]
            error_msg = f"필수 필드가 누락되었습니다: {missing_field}"
        elif "is not one of" in error_msg:
            error_msg = "허용되지 않는 값입니다"
        
        raise ValidationError(f"데이터 검증 실패: {error_msg}")


def validate_fortune_request(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    운세 요청 데이터 검증 (간단한 버전)
    
    Args:
        data: 검증할 요청 데이터
        
    Returns:
        Dict: {"valid": bool, "error": str}
    """
    try:
        if not data:
            return {"valid": False, "error": "요청 데이터가 비어있습니다"}
        
        # 기본 필드 확인
        if "mode" not in data:
            return {"valid": False, "error": "mode 필드가 필요합니다"}
        
        if "participants" not in data:
            return {"valid": False, "error": "participants 필드가 필요합니다"}
        
        mode = data["mode"]
        participants = data["participants"]
        
        # 모드 검증
        if mode not in ["individual", "group"]:
            return {"valid": False, "error": "mode는 'individual' 또는 'group'이어야 합니다"}
        
        # 참석자 수 검증
        if not isinstance(participants, list):
            return {"valid": False, "error": "participants는 배열이어야 합니다"}
        
        if mode == "individual" and len(participants) != 1:
            return {"valid": False, "error": "개인 모드에서는 정확히 1명의 참석자가 필요합니다"}
        
        if mode == "group" and len(participants) < 2:
            return {"valid": False, "error": "그룹 모드에서는 최소 2명의 참석자가 필요합니다"}
        
        if len(participants) > 10:
            return {"valid": False, "error": "최대 10명까지만 가능합니다"}
        
        # 각 참석자 데이터 검증
        for i, participant in enumerate(participants):
            if not isinstance(participant, dict):
                return {"valid": False, "error": f"참석자 {i+1}의 데이터가 올바르지 않습니다"}
            
            if "birth_date" not in participant:
                return {"valid": False, "error": f"참석자 {i+1}의 생년월일이 필요합니다"}
            
            birth_date = participant["birth_date"]
            
            # 날짜 형식 검증
            try:
                datetime.strptime(birth_date, "%Y-%m-%d")
            except ValueError:
                return {"valid": False, "error": f"참석자 {i+1}의 생년월일 형식이 올바르지 않습니다 (YYYY-MM-DD)"}
            
            # 미래 날짜 검증
            birth_date_obj = datetime.strptime(birth_date, "%Y-%m-%d").date()
            current_date = datetime.now().date()
            
            if birth_date_obj > current_date:
                return {"valid": False, "error": f"참석자 {i+1}의 생년월일은 미래 날짜일 수 없습니다"}
            
            # 너무 오래된 날짜 검증
            if birth_date_obj.year < 1900:
                return {"valid": False, "error": f"참석자 {i+1}의 생년월일이 너무 오래되었습니다"}
        
        return {"valid": True, "error": ""}
        
    except Exception as e:
        return {"valid": False, "error": f"검증 중 오류가 발생했습니다: {str(e)}"}


# 검증 데코레이터
def validate_request(validation_type: str):
    """
    Flask 라우트에서 사용할 검증 데코레이터
    
    Args:
        validation_type: 검증 타입
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            from flask import request, jsonify
            
            try:
                if request.is_json:
                    data = request.get_json()
                    validate_json_data(data, validation_type)
                else:
                    return jsonify({"error": "Content-Type은 application/json이어야 합니다"}), 400
                    
            except ValidationError as e:
                return jsonify({"error": str(e)}), 400
            except Exception as e:
                return jsonify({"error": f"요청 처리 중 오류가 발생했습니다: {str(e)}"}), 500
            
            return func(*args, **kwargs)
        
        wrapper.__name__ = func.__name__
        return wrapper
    return decorator