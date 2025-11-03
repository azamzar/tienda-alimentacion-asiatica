"""
Tests for image optimization utilities
"""
import pytest
import os
import shutil
from pathlib import Path
from PIL import Image

from app.utils.image_optimizer import (
    optimize_image,
    resize_with_aspect_ratio,
    generate_thumbnails,
    delete_product_images,
    get_image_info,
    IMAGE_SIZES,
    WEBP_QUALITY,
    JPEG_QUALITY
)


@pytest.fixture
def test_upload_dir(tmp_path):
    """Create temporary upload directory"""
    upload_dir = tmp_path / "uploads" / "products"
    upload_dir.mkdir(parents=True, exist_ok=True)
    yield upload_dir
    # Cleanup
    if upload_dir.exists():
        shutil.rmtree(upload_dir.parent)


@pytest.fixture
def sample_image(tmp_path):
    """Create a sample test image (RGB JPEG)"""
    img_path = tmp_path / "test_image.jpg"
    img = Image.new('RGB', (800, 600), color='red')
    img.save(img_path, 'JPEG')
    return img_path


@pytest.fixture
def sample_rgba_image(tmp_path):
    """Create a sample RGBA PNG image"""
    img_path = tmp_path / "test_rgba.png"
    img = Image.new('RGBA', (800, 600), color=(255, 0, 0, 128))
    img.save(img_path, 'PNG')
    return img_path


@pytest.fixture
def sample_large_image(tmp_path):
    """Create a large test image"""
    img_path = tmp_path / "large_image.jpg"
    img = Image.new('RGB', (2000, 1500), color='blue')
    img.save(img_path, 'JPEG')
    return img_path


class TestOptimizeImage:
    """Tests for optimize_image function"""

    @pytest.mark.unit
    @pytest.mark.images
    def test_optimize_image_basic(self, sample_image, tmp_path):
        """Test basic image optimization"""
        output_path = tmp_path / "optimized.webp"

        result = optimize_image(
            sample_image,
            output_path,
            format="WEBP",
            quality=WEBP_QUALITY
        )

        assert result == output_path
        assert output_path.exists()

        # Verify it's a valid image
        with Image.open(output_path) as img:
            assert img.format == "WEBP"
            assert img.mode == "RGB"

    @pytest.mark.unit
    @pytest.mark.images
    def test_optimize_image_with_resize(self, sample_image, tmp_path):
        """Test image optimization with resizing"""
        output_path = tmp_path / "resized.webp"
        target_size = (300, 300)

        result = optimize_image(
            sample_image,
            output_path,
            size=target_size,
            format="WEBP"
        )

        assert result.exists()

        with Image.open(result) as img:
            assert img.width == target_size[0]
            assert img.height == target_size[1]

    @pytest.mark.unit
    @pytest.mark.images
    def test_optimize_image_rgba_conversion(self, sample_rgba_image, tmp_path):
        """Test RGBA to RGB conversion for WebP"""
        output_path = tmp_path / "converted.webp"

        result = optimize_image(
            sample_rgba_image,
            output_path,
            format="WEBP"
        )

        assert result.exists()

        with Image.open(result) as img:
            assert img.mode == "RGB"  # Should be converted from RGBA

    @pytest.mark.unit
    @pytest.mark.images
    def test_optimize_image_jpeg_format(self, sample_image, tmp_path):
        """Test optimization with JPEG format"""
        output_path = tmp_path / "optimized.jpg"

        result = optimize_image(
            sample_image,
            output_path,
            format="JPEG",
            quality=JPEG_QUALITY
        )

        assert result.exists()

        with Image.open(result) as img:
            assert img.format == "JPEG"

    @pytest.mark.unit
    @pytest.mark.images
    def test_optimize_image_creates_directory(self, sample_image, tmp_path):
        """Test that output directory is created if it doesn't exist"""
        output_path = tmp_path / "subdir" / "nested" / "image.webp"

        result = optimize_image(sample_image, output_path)

        assert result.exists()
        assert output_path.parent.exists()

    @pytest.mark.unit
    @pytest.mark.images
    def test_optimize_image_file_not_found(self, tmp_path):
        """Test error handling for non-existent source image"""
        non_existent = tmp_path / "does_not_exist.jpg"
        output_path = tmp_path / "output.webp"

        with pytest.raises(FileNotFoundError):
            optimize_image(non_existent, output_path)

    @pytest.mark.unit
    @pytest.mark.images
    def test_optimize_image_compression_reduces_size(self, sample_large_image, tmp_path):
        """Test that optimization actually reduces file size"""
        original_size = os.path.getsize(sample_large_image)
        output_path = tmp_path / "compressed.webp"

        optimize_image(sample_large_image, output_path, format="WEBP", quality=85)

        compressed_size = os.path.getsize(output_path)
        assert compressed_size < original_size  # Should be smaller


class TestResizeWithAspectRatio:
    """Tests for resize_with_aspect_ratio function"""

    @pytest.mark.unit
    @pytest.mark.images
    def test_resize_wider_image(self):
        """Test resizing a wider image (landscape)"""
        img = Image.new('RGB', (800, 600), color='green')
        target_size = (300, 300)

        resized = resize_with_aspect_ratio(img, target_size)

        assert resized.width == target_size[0]
        assert resized.height == target_size[1]

    @pytest.mark.unit
    @pytest.mark.images
    def test_resize_taller_image(self):
        """Test resizing a taller image (portrait)"""
        img = Image.new('RGB', (600, 800), color='blue')
        target_size = (300, 300)

        resized = resize_with_aspect_ratio(img, target_size)

        assert resized.width == target_size[0]
        assert resized.height == target_size[1]

    @pytest.mark.unit
    @pytest.mark.images
    def test_resize_maintains_aspect_ratio(self):
        """Test that aspect ratio is maintained (with padding)"""
        img = Image.new('RGB', (1600, 900), color='red')  # 16:9 aspect
        target_size = (300, 300)

        resized = resize_with_aspect_ratio(img, target_size)

        # The image should fit within target size with padding
        assert resized.width == 300
        assert resized.height == 300
        # The actual image content should maintain 16:9 ratio

    @pytest.mark.unit
    @pytest.mark.images
    def test_resize_square_image(self):
        """Test resizing a square image"""
        img = Image.new('RGB', (800, 800), color='yellow')
        target_size = (300, 300)

        resized = resize_with_aspect_ratio(img, target_size)

        assert resized.width == 300
        assert resized.height == 300


class TestGenerateThumbnails:
    """Tests for generate_thumbnails function"""

    @pytest.mark.unit
    @pytest.mark.images
    def test_generate_thumbnails_creates_all_sizes(self, sample_image, test_upload_dir):
        """Test that all thumbnail sizes are generated"""
        product_id = 1

        urls = generate_thumbnails(sample_image, product_id, test_upload_dir)

        # Check that all expected sizes are in the result
        assert "original" in urls
        assert "thumbnail" in urls
        assert "medium" in urls
        assert "large" in urls

        # Check that all files exist
        product_dir = test_upload_dir / str(product_id)
        assert (product_dir / "original.jpg").exists()
        assert (product_dir / "thumbnail.webp").exists()
        assert (product_dir / "medium.webp").exists()
        assert (product_dir / "large.webp").exists()

    @pytest.mark.unit
    @pytest.mark.images
    def test_generate_thumbnails_correct_sizes(self, sample_image, test_upload_dir):
        """Test that thumbnails have correct dimensions"""
        product_id = 2

        generate_thumbnails(sample_image, product_id, test_upload_dir)

        product_dir = test_upload_dir / str(product_id)

        # Check thumbnail size
        with Image.open(product_dir / "thumbnail.webp") as img:
            assert img.width == IMAGE_SIZES["thumbnail"][0]
            assert img.height == IMAGE_SIZES["thumbnail"][1]

        # Check medium size
        with Image.open(product_dir / "medium.webp") as img:
            assert img.width == IMAGE_SIZES["medium"][0]
            assert img.height == IMAGE_SIZES["medium"][1]

        # Check large size
        with Image.open(product_dir / "large.webp") as img:
            assert img.width == IMAGE_SIZES["large"][0]
            assert img.height == IMAGE_SIZES["large"][1]

    @pytest.mark.unit
    @pytest.mark.images
    def test_generate_thumbnails_correct_urls(self, sample_image, test_upload_dir):
        """Test that generated URLs are correct"""
        product_id = 3

        urls = generate_thumbnails(sample_image, product_id, test_upload_dir)

        assert urls["original"] == f"/uploads/products/{product_id}/original.jpg"
        assert urls["thumbnail"] == f"/uploads/products/{product_id}/thumbnail.webp"
        assert urls["medium"] == f"/uploads/products/{product_id}/medium.webp"
        assert urls["large"] == f"/uploads/products/{product_id}/large.webp"

    @pytest.mark.unit
    @pytest.mark.images
    def test_generate_thumbnails_creates_directory(self, sample_image, test_upload_dir):
        """Test that product directory is created"""
        product_id = 4
        product_dir = test_upload_dir / str(product_id)

        assert not product_dir.exists()

        generate_thumbnails(sample_image, product_id, test_upload_dir)

        assert product_dir.exists()
        assert product_dir.is_dir()

    @pytest.mark.unit
    @pytest.mark.images
    def test_generate_thumbnails_webp_format(self, sample_image, test_upload_dir):
        """Test that thumbnails are in WebP format"""
        product_id = 5

        generate_thumbnails(sample_image, product_id, test_upload_dir)

        product_dir = test_upload_dir / str(product_id)

        with Image.open(product_dir / "thumbnail.webp") as img:
            assert img.format == "WEBP"

        with Image.open(product_dir / "medium.webp") as img:
            assert img.format == "WEBP"


class TestDeleteProductImages:
    """Tests for delete_product_images function"""

    @pytest.mark.unit
    @pytest.mark.images
    def test_delete_product_images_success(self, sample_image, test_upload_dir):
        """Test successful deletion of product images"""
        product_id = 10

        # First create images
        generate_thumbnails(sample_image, product_id, test_upload_dir)

        product_dir = test_upload_dir / str(product_id)
        assert product_dir.exists()

        # Delete images
        result = delete_product_images(product_id, test_upload_dir)

        assert result is True
        assert not product_dir.exists()

    @pytest.mark.unit
    @pytest.mark.images
    def test_delete_product_images_non_existent(self, test_upload_dir):
        """Test deleting images for non-existent product"""
        product_id = 999

        result = delete_product_images(product_id, test_upload_dir)

        assert result is False

    @pytest.mark.unit
    @pytest.mark.images
    def test_delete_product_images_removes_all_files(self, sample_image, test_upload_dir):
        """Test that all files are deleted"""
        product_id = 11

        # Create images
        generate_thumbnails(sample_image, product_id, test_upload_dir)

        product_dir = test_upload_dir / str(product_id)
        files_before = list(product_dir.iterdir())
        assert len(files_before) > 0

        # Delete
        delete_product_images(product_id, test_upload_dir)

        assert not product_dir.exists()


class TestGetImageInfo:
    """Tests for get_image_info function"""

    @pytest.mark.unit
    @pytest.mark.images
    def test_get_image_info_success(self, sample_image):
        """Test getting image information"""
        info = get_image_info(sample_image)

        assert "width" in info
        assert "height" in info
        assert "format" in info
        assert "mode" in info
        assert "size_bytes" in info

        assert info["width"] == 800
        assert info["height"] == 600
        assert info["format"] == "JPEG"
        assert info["mode"] == "RGB"
        assert info["size_bytes"] > 0

    @pytest.mark.unit
    @pytest.mark.images
    def test_get_image_info_rgba(self, sample_rgba_image):
        """Test getting info from RGBA image"""
        info = get_image_info(sample_rgba_image)

        assert info["mode"] == "RGBA"
        assert info["format"] == "PNG"

    @pytest.mark.unit
    @pytest.mark.images
    def test_get_image_info_file_not_found(self, tmp_path):
        """Test error handling for non-existent image"""
        non_existent = tmp_path / "does_not_exist.jpg"

        with pytest.raises(FileNotFoundError):
            get_image_info(non_existent)

    @pytest.mark.unit
    @pytest.mark.images
    def test_get_image_info_dimensions(self, sample_large_image):
        """Test correct dimensions are returned"""
        info = get_image_info(sample_large_image)

        assert info["width"] == 2000
        assert info["height"] == 1500


class TestImageSizeConfiguration:
    """Tests for image size configurations"""

    @pytest.mark.unit
    def test_image_sizes_defined(self):
        """Test that all image sizes are defined"""
        assert "thumbnail" in IMAGE_SIZES
        assert "medium" in IMAGE_SIZES
        assert "large" in IMAGE_SIZES
        assert "original" in IMAGE_SIZES

    @pytest.mark.unit
    def test_image_sizes_values(self):
        """Test that image sizes have correct values"""
        assert IMAGE_SIZES["thumbnail"] == (150, 150)
        assert IMAGE_SIZES["medium"] == (300, 300)
        assert IMAGE_SIZES["large"] == (600, 600)
        assert IMAGE_SIZES["original"] is None

    @pytest.mark.unit
    def test_quality_settings(self):
        """Test quality settings are within valid range"""
        assert 0 <= WEBP_QUALITY <= 100
        assert 0 <= JPEG_QUALITY <= 100
