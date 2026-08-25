from fastapi import HTTPException
from datetime import datetime, timezone


def _error_response(
    status_code: int,
    message: str,
):
    return {
        "status": "error",
        "status_code": status_code,
        "message": message,
        "created_at": datetime.now(timezone.utc).isoformat()
    }


def bad_request(
    detail="Dữ liệu không hợp lệ",
):
    raise HTTPException(
        status_code=400,
        detail=_error_response(
            400,
            detail,
            
        )
    )


def unauthorized(
    detail="Bạn chưa được xác thực",
):
    raise HTTPException(
        status_code=401,
        detail=_error_response(
            401,
            detail,
            
        )
    )


def forbidden(
    detail="Bạn không có quyền truy cập",
):
    raise HTTPException(
        status_code=403,
        detail=_error_response(
            403,
            detail,
            
        )
    )


def not_found(
    detail="Không tìm thấy tài nguyên",
):
    raise HTTPException(
        status_code=404,
        detail=_error_response(
            404,
            detail,
            
        )
    )