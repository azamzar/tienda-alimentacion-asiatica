"""
Image optimization utilities for product images.
Handles thumbnail generation, WebP conversion, and image optimization.
"""
from typing import Tuple, Optional
from pathlib import Path
from PIL import Image
import os

# Image size configurations (width, height)
IMAGE_SIZES = {
    "thumbnail": (150, 150),    # For list views, cart items
    "medium": (300, 300),        # For product cards
    "large": (600, 600),         # For product detail page
    "original": None             # Keep original size
}

# WebP quality settings (0-100)
WEBP_QUALITY = 85

# JPEG quality settings (0-100)
JPEG_QUALITY = 90


def optimize_image(
    image_path: Path,
    output_path: Path,
    size: Optional[Tuple[int, int]] = None,
    format: str = "WEBP",
    quality: int = WEBP_QUALITY
) -> Path:
    """
    Optimize and resize an image.

    Args:
        image_path: Path to the source image
        output_path: Path where to save the optimized image
        size: Target size (width, height). If None, keeps original size
        format: Output format (WEBP, JPEG, PNG)
        quality: Quality setting (0-100)

    Returns:
        Path to the optimized image

    Raises:
        FileNotFoundError: If source image doesn't exist
        ValueError: If image format is invalid
    """
    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    # Open and convert image to RGB (needed for WebP)
    with Image.open(image_path) as img:
        # Convert RGBA to RGB if needed (for WebP compatibility)
        if img.mode in ('RGBA', 'LA', 'P'):
            # Create white background
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')

        # Resize if size is specified
        if size:
            img = resize_with_aspect_ratio(img, size)

        # Create output directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Save with optimization
        save_kwargs = {
            "optimize": True,
            "quality": quality
        }

        if format.upper() == "WEBP":
            save_kwargs["method"] = 6  # Maximum compression effort
        elif format.upper() == "JPEG":
            save_kwargs["progressive"] = True

        img.save(output_path, format=format, **save_kwargs)

    return output_path


def resize_with_aspect_ratio(
    image: Image.Image,
    target_size: Tuple[int, int]
) -> Image.Image:
    """
    Resize image maintaining aspect ratio.
    Fits the image within the target size, adding padding if needed.

    Args:
        image: PIL Image object
        target_size: Target size (width, height)

    Returns:
        Resized PIL Image object
    """
    # Calculate aspect ratios
    img_ratio = image.width / image.height
    target_ratio = target_size[0] / target_size[1]

    if img_ratio > target_ratio:
        # Image is wider - fit to width
        new_width = target_size[0]
        new_height = int(new_width / img_ratio)
    else:
        # Image is taller - fit to height
        new_height = target_size[1]
        new_width = int(new_height * img_ratio)

    # Resize image using high-quality Lanczos resampling
    resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Create white background with target size
    background = Image.new('RGB', target_size, (255, 255, 255))

    # Calculate position to center the image
    x = (target_size[0] - new_width) // 2
    y = (target_size[1] - new_height) // 2

    # Paste resized image onto background
    background.paste(resized, (x, y))

    return background


def generate_thumbnails(
    source_image_path: Path,
    product_id: int,
    upload_dir: Path
) -> dict[str, str]:
    """
    Generate all thumbnail sizes and WebP versions for a product image.

    Directory structure created:
    uploads/products/{product_id}/
        ├── original.jpg
        ├── thumbnail.webp (150x150)
        ├── medium.webp (300x300)
        └── large.webp (600x600)

    Args:
        source_image_path: Path to the original uploaded image
        product_id: ID of the product
        upload_dir: Base upload directory (e.g., 'uploads/products')

    Returns:
        Dictionary with URLs for each size:
        {
            "original": "/uploads/products/{id}/original.jpg",
            "thumbnail": "/uploads/products/{id}/thumbnail.webp",
            "medium": "/uploads/products/{id}/medium.webp",
            "large": "/uploads/products/{id}/large.webp"
        }

    Raises:
        FileNotFoundError: If source image doesn't exist
        OSError: If there's an error creating directories or saving files
    """
    # Create product-specific directory
    product_dir = upload_dir / str(product_id)
    product_dir.mkdir(parents=True, exist_ok=True)

    # Get original file extension
    original_ext = source_image_path.suffix

    # Copy/optimize original image
    original_path = product_dir / f"original{original_ext}"
    optimize_image(
        source_image_path,
        original_path,
        size=None,  # Keep original size
        format="JPEG" if original_ext.lower() in ['.jpg', '.jpeg'] else "PNG",
        quality=JPEG_QUALITY
    )

    # Generate thumbnails in WebP format
    urls = {
        "original": f"/uploads/products/{product_id}/original{original_ext}"
    }

    for size_name, size_dimensions in IMAGE_SIZES.items():
        if size_name == "original":
            continue

        output_path = product_dir / f"{size_name}.webp"
        optimize_image(
            source_image_path,
            output_path,
            size=size_dimensions,
            format="WEBP",
            quality=WEBP_QUALITY
        )

        urls[size_name] = f"/uploads/products/{product_id}/{size_name}.webp"

    return urls


def delete_product_images(product_id: int, upload_dir: Path) -> bool:
    """
    Delete all images (original + thumbnails) for a product.

    Args:
        product_id: ID of the product
        upload_dir: Base upload directory (e.g., 'uploads/products')

    Returns:
        True if deletion was successful, False otherwise
    """
    product_dir = upload_dir / str(product_id)

    if not product_dir.exists():
        return False

    try:
        # Delete all files in product directory
        for file in product_dir.iterdir():
            if file.is_file():
                file.unlink()

        # Remove the directory
        product_dir.rmdir()
        return True
    except Exception as e:
        print(f"Error deleting images for product {product_id}: {e}")
        return False


def get_image_info(image_path: Path) -> dict:
    """
    Get information about an image file.

    Args:
        image_path: Path to the image file

    Returns:
        Dictionary with image information:
        {
            "width": int,
            "height": int,
            "format": str,
            "mode": str,
            "size_bytes": int
        }
    """
    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    with Image.open(image_path) as img:
        return {
            "width": img.width,
            "height": img.height,
            "format": img.format,
            "mode": img.mode,
            "size_bytes": os.path.getsize(image_path)
        }
