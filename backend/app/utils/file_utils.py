"""
File handling utilities for image uploads
"""
import os
import uuid
from pathlib import Path
from typing import Optional
from fastapi import UploadFile, HTTPException

# Allowed image extensions
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}

# Max file size: 5MB
MAX_FILE_SIZE = 5 * 1024 * 1024


def validate_image_file(file: UploadFile) -> None:
    """
    Validate uploaded image file

    Args:
        file: The uploaded file

    Raises:
        HTTPException: If file is invalid
    """
    # Check if file has a filename
    if not file.filename:
        raise HTTPException(status_code=400, detail="No se proporcionó ningún archivo")

    # Check file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Formato de archivo no permitido. Use: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    # Check content type
    if file.content_type not in ["image/jpeg", "image/png", "image/gif", "image/webp"]:
        raise HTTPException(
            status_code=400,
            detail="Tipo de contenido no válido. Solo se permiten imágenes."
        )


def generate_unique_filename(original_filename: str) -> str:
    """
    Generate unique filename using UUID

    Args:
        original_filename: Original uploaded filename

    Returns:
        Unique filename with original extension
    """
    file_ext = Path(original_filename).suffix.lower()
    unique_name = f"{uuid.uuid4()}{file_ext}"
    return unique_name


async def save_upload_file(
    upload_file: UploadFile,
    destination_dir: Path,
    max_size: int = MAX_FILE_SIZE
) -> str:
    """
    Save uploaded file to destination directory

    Args:
        upload_file: The uploaded file
        destination_dir: Directory to save file
        max_size: Maximum file size in bytes

    Returns:
        The saved filename

    Raises:
        HTTPException: If file is too large or save fails
    """
    # Validate file
    validate_image_file(upload_file)

    # Create directory if it doesn't exist
    destination_dir.mkdir(parents=True, exist_ok=True)

    # Generate unique filename
    filename = generate_unique_filename(upload_file.filename)
    file_path = destination_dir / filename

    # Save file with size check
    try:
        contents = await upload_file.read()

        # Check file size
        if len(contents) > max_size:
            raise HTTPException(
                status_code=400,
                detail=f"El archivo es demasiado grande. Tamaño máximo: {max_size / 1024 / 1024}MB"
            )

        # Write file
        with open(file_path, "wb") as f:
            f.write(contents)

        return filename

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al guardar el archivo: {str(e)}"
        )
    finally:
        await upload_file.close()


def delete_file(file_path: Path) -> bool:
    """
    Delete file if it exists

    Args:
        file_path: Path to file

    Returns:
        True if file was deleted, False if file didn't exist
    """
    try:
        if file_path.exists():
            file_path.unlink()
            return True
        return False
    except Exception:
        return False
