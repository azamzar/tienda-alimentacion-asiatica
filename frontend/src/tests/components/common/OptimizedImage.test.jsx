import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import OptimizedImage from '../../../components/common/OptimizedImage';

describe('OptimizedImage', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe('Basic rendering', () => {
    it('renders with default props', async () => {
      render(<OptimizedImage src="http://example.com/image.jpg" alt="Test image" />);

      await waitFor(() => {
        const container = screen.getByAltText('Test image').closest('.optimized-image');
        expect(container).toBeInTheDocument();
      });
    });

    it('renders with custom className', async () => {
      render(
        <OptimizedImage
          src="http://example.com/image.jpg"
          alt="Test"
          className="custom-class"
        />
      );

      await waitFor(() => {
        const container = screen.getByAltText('Test').closest('.optimized-image');
        expect(container).toHaveClass('custom-class');
      });
    });

    it('uses fallback alt text when not provided', async () => {
      render(<OptimizedImage src="http://example.com/image.jpg" />);

      await waitFor(() => {
        expect(screen.getByAltText('Product image')).toBeInTheDocument();
      });
    });
  });

  describe('Lazy loading', () => {
    it('renders placeholder when lazy loading is enabled and not in view', async () => {
      // Mock IntersectionObserver to not trigger immediately
      const mockObserve = vi.fn();
      global.IntersectionObserver = class MockIntersectionObserver {
        constructor(callback, options) {
          this.callback = callback;
          this.options = options;
        }
        observe(target) {
          mockObserve(target);
          // Don't trigger callback - image should not load
        }
        unobserve() {}
        disconnect() {}
      };

      const { container } = render(
        <OptimizedImage src="http://example.com/image.jpg" alt="Test" lazy={true} />
      );

      const placeholder = container.querySelector('.optimized-image__placeholder');
      expect(placeholder).toBeInTheDocument();
    });

    it('loads image when lazy=false', async () => {
      render(
        <OptimizedImage
          src="http://example.com/image.jpg"
          alt="Test image"
          lazy={false}
        />
      );

      await waitFor(() => {
        expect(screen.getByAltText('Test image')).toBeInTheDocument();
      });
    });

    it('loads image when it enters viewport', async () => {
      let observerCallback;

      global.IntersectionObserver = class MockIntersectionObserver {
        constructor(callback) {
          observerCallback = callback;
        }
        observe() {
          // Simulate image entering viewport
          setTimeout(() => {
            observerCallback([{ isIntersecting: true }]);
          }, 10);
        }
        unobserve() {}
        disconnect() {}
      };

      render(
        <OptimizedImage
          src="http://example.com/image.jpg"
          alt="Test"
          lazy={true}
        />
      );

      await waitFor(() => {
        expect(screen.getByAltText('Test')).toBeInTheDocument();
      }, { timeout: 200 });
    });
  });

  describe('Image source handling', () => {
    it('handles external HTTP URLs correctly', async () => {
      render(
        <OptimizedImage
          src="http://example.com/image.jpg"
          alt="Test"
          lazy={false}
        />
      );

      await waitFor(() => {
        const img = screen.getByAltText('Test');
        expect(img.src).toContain('http://example.com/image.jpg');
      });
    });

    it('handles external HTTPS URLs correctly', async () => {
      render(
        <OptimizedImage
          src="https://example.com/image.jpg"
          alt="Test"
          lazy={false}
        />
      );

      await waitFor(() => {
        const img = screen.getByAltText('Test');
        expect(img.src).toContain('https://example.com/image.jpg');
      });
    });

    it('generates optimized URLs when productId is provided', async () => {
      render(
        <OptimizedImage
          src="/uploads/products/1/large.webp"
          productId={1}
          size="medium"
          alt="Test"
          lazy={false}
        />
      );

      await waitFor(() => {
        const img = screen.getByAltText('Test');
        expect(img.src).toContain('/products/1/medium.webp');
      });
    });

    it('handles /uploads/ paths correctly', async () => {
      render(
        <OptimizedImage
          src="/uploads/products/test.jpg"
          alt="Test"
          lazy={false}
        />
      );

      await waitFor(() => {
        const img = screen.getByAltText('Test');
        expect(img.src).toContain('localhost:8000/uploads/products/test.jpg');
      });
    });

    it('uses fallback image when src is not provided', async () => {
      render(
        <OptimizedImage
          alt="Test"
          lazy={false}
          fallback="http://example.com/fallback.jpg"
        />
      );

      await waitFor(() => {
        const img = screen.getByAltText('Test');
        expect(img.src).toContain('fallback.jpg');
      });
    });
  });

  describe('Image sizes', () => {
    it.each([
      ['thumbnail', 'thumbnail'],
      ['medium', 'medium'],
      ['large', 'large'],
    ])('handles %s size correctly', async (size, expected) => {
      render(
        <OptimizedImage
          src="/uploads/products/1/image.jpg"
          productId={1}
          size={size}
          alt="Test"
          lazy={false}
        />
      );

      await waitFor(() => {
        const img = screen.getByAltText('Test');
        expect(img.src).toContain(`/${expected}.webp`);
      });
    });
  });

  describe('Error handling', () => {
    it('displays fallback image on load error', async () => {
      // Mock Image to always fail
      const originalImage = global.Image;
      global.Image = class MockImage {
        set src(value) {
          setTimeout(() => {
            this.onerror && this.onerror();
          }, 10);
        }
      };

      render(
        <OptimizedImage
          src="http://example.com/broken.jpg"
          alt="Test"
          fallback="http://example.com/fallback.jpg"
          lazy={false}
        />
      );

      await waitFor(() => {
        const img = screen.getByAltText('Test');
        expect(img.src).toContain('fallback.jpg');
      }, { timeout: 200 });

      global.Image = originalImage;
    });

    it('handles image error event', async () => {
      render(
        <OptimizedImage
          src="http://example.com/image.jpg"
          alt="Test"
          fallback="http://example.com/fallback.jpg"
          lazy={false}
        />
      );

      await waitFor(() => {
        const img = screen.getByAltText('Test');
        expect(img).toBeInTheDocument();
      });

      // Trigger error on the img element
      const img = screen.getByAltText('Test');
      const errorEvent = new Event('error');
      img.dispatchEvent(errorEvent);

      await waitFor(() => {
        expect(img.src).toContain('fallback.jpg');
      });
    });
  });

  describe('Responsive images', () => {
    it('generates srcset when productId is provided', async () => {
      render(
        <OptimizedImage
          src="/uploads/products/1/image.jpg"
          productId={1}
          size="medium"
          alt="Test"
          lazy={false}
        />
      );

      await waitFor(() => {
        const img = screen.getByAltText('Test');
        expect(img).toHaveAttribute('srcset');
        expect(img.srcset).toContain('thumbnail.webp 150w');
        expect(img.srcset).toContain('medium.webp 300w');
        expect(img.srcset).toContain('large.webp 600w');
      });
    });

    it('does not generate srcset when productId is not provided', async () => {
      render(
        <OptimizedImage
          src="http://example.com/image.jpg"
          alt="Test"
          lazy={false}
        />
      );

      await waitFor(() => {
        const img = screen.getByAltText('Test');
        expect(img).not.toHaveAttribute('srcset');
      });
    });

    it('generates correct sizes attribute for different image sizes', async () => {
      const { rerender } = render(
        <OptimizedImage
          src="/uploads/products/1/image.jpg"
          productId={1}
          size="thumbnail"
          alt="Test"
          lazy={false}
        />
      );

      await waitFor(() => {
        const img = screen.getByAltText('Test');
        expect(img.sizes).toBe('150px');
      });

      rerender(
        <OptimizedImage
          src="/uploads/products/1/image.jpg"
          productId={1}
          size="medium"
          alt="Test"
          lazy={false}
        />
      );

      await waitFor(() => {
        const img = screen.getByAltText('Test');
        expect(img.sizes).toBe('(max-width: 768px) 100vw, 300px');
      });

      rerender(
        <OptimizedImage
          src="/uploads/products/1/image.jpg"
          productId={1}
          size="large"
          alt="Test"
          lazy={false}
        />
      );

      await waitFor(() => {
        const img = screen.getByAltText('Test');
        expect(img.sizes).toBe('(max-width: 768px) 100vw, 600px');
      });
    });
  });

  describe('Loading states', () => {
    it('shows loading class initially', () => {
      const { container } = render(
        <OptimizedImage
          src="http://example.com/image.jpg"
          alt="Test"
          lazy={false}
        />
      );

      const wrapper = container.querySelector('.optimized-image');
      expect(wrapper).toHaveClass('loading');
    });

    it('shows loaded class after image loads', async () => {
      const { container } = render(
        <OptimizedImage
          src="http://example.com/image.jpg"
          alt="Test"
          lazy={false}
        />
      );

      await waitFor(() => {
        const wrapper = container.querySelector('.optimized-image');
        expect(wrapper).toHaveClass('loaded');
      }, { timeout: 200 });
    });

    it('shows loader while image is loading', async () => {
      // Mock Image to delay loading
      const originalImage = global.Image;
      global.Image = class MockImage {
        set src(value) {
          // Delay the onload event
          setTimeout(() => {
            this.onload && this.onload();
          }, 100);
        }
      };

      const { container } = render(
        <OptimizedImage
          src="http://example.com/image.jpg"
          alt="Test"
          lazy={false}
        />
      );

      // Initially should show loader
      await waitFor(() => {
        const loader = container.querySelector('.optimized-image__loader');
        expect(loader).toBeInTheDocument();
      }, { timeout: 50 });

      global.Image = originalImage;
    });
  });

  describe('Progressive loading', () => {
    it('loads thumbnail first for non-thumbnail sizes', async () => {
      const loadedImages = [];

      const originalImage = global.Image;
      global.Image = class MockImage {
        set src(value) {
          loadedImages.push(value);
          setTimeout(() => {
            this.onload && this.onload();
          }, 10);
        }
      };

      render(
        <OptimizedImage
          src="/uploads/products/1/image.jpg"
          productId={1}
          size="large"
          alt="Test"
          lazy={false}
        />
      );

      await waitFor(() => {
        expect(loadedImages.length).toBeGreaterThan(0);
      }, { timeout: 200 });

      // Should load thumbnail first, then large
      expect(loadedImages.some(url => url.includes('thumbnail.webp'))).toBe(true);
      expect(loadedImages.some(url => url.includes('large.webp'))).toBe(true);

      global.Image = originalImage;
    });
  });

  describe('Loading attribute', () => {
    it('sets loading="lazy" when lazy is true', async () => {
      render(
        <OptimizedImage
          src="http://example.com/image.jpg"
          alt="Test"
          lazy={true}
        />
      );

      await waitFor(() => {
        const img = screen.getByAltText('Test');
        expect(img).toHaveAttribute('loading', 'lazy');
      });
    });

    it('sets loading="eager" when lazy is false', async () => {
      render(
        <OptimizedImage
          src="http://example.com/image.jpg"
          alt="Test"
          lazy={false}
        />
      );

      await waitFor(() => {
        const img = screen.getByAltText('Test');
        expect(img).toHaveAttribute('loading', 'eager');
      });
    });
  });
});
