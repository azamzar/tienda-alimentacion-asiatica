import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import ProductCard from '../../../components/products/ProductCard';
import { useCartStore } from '../../../store/useCartStore';

// Mock the stores
vi.mock('../../../store/useCartStore');

// Mock useNavigate
const mockNavigate = vi.fn();
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual,
    useNavigate: () => mockNavigate,
  };
});

// Mock OptimizedImage to simplify testing
vi.mock('../../../components/common/OptimizedImage', () => ({
  default: ({ alt, src }) => <img alt={alt} src={src} />,
}));

const renderWithRouter = (component) => {
  return render(<BrowserRouter>{component}</BrowserRouter>);
};

describe('ProductCard', () => {
  const mockAddItem = vi.fn();

  const mockProduct = {
    id: 1,
    name: 'Salsa Soja Premium',
    description: 'Salsa de soja japonesa de alta calidad',
    price: 4.99,
    stock: 50,
    category_id: 1,
    image_url: '/uploads/products/1/large.webp',
    category: {
      id: 1,
      name: 'Salsas',
    },
  };

  beforeEach(() => {
    vi.clearAllMocks();
    mockNavigate.mockClear();

    // Setup default cart store mock
    useCartStore.mockReturnValue({
      addItem: mockAddItem,
    });
  });

  describe('Rendering', () => {
    it('renders product information correctly', () => {
      renderWithRouter(<ProductCard product={mockProduct} />);

      expect(screen.getByText('Salsa Soja Premium')).toBeInTheDocument();
      expect(screen.getByText('Salsa de soja japonesa de alta calidad')).toBeInTheDocument();
      expect(screen.getByText('4,99 €')).toBeInTheDocument();
      expect(screen.getByText('Salsas')).toBeInTheDocument();
      expect(screen.getByText(/Stock:/)).toBeInTheDocument();
      expect(screen.getByText('50')).toBeInTheDocument();
    });

    it('renders product image', () => {
      renderWithRouter(<ProductCard product={mockProduct} />);

      const image = screen.getByAltText('Salsa Soja Premium');
      expect(image).toBeInTheDocument();
    });

    it('renders category when provided', () => {
      renderWithRouter(<ProductCard product={mockProduct} />);

      expect(screen.getByText('Salsas')).toBeInTheDocument();
    });

    it('does not render category when not provided', () => {
      const productWithoutCategory = { ...mockProduct, category: null };
      renderWithRouter(<ProductCard product={productWithoutCategory} />);

      expect(screen.queryByText('Salsas')).not.toBeInTheDocument();
    });

    it('does not render description when not provided', () => {
      const productWithoutDescription = { ...mockProduct, description: null };
      renderWithRouter(<ProductCard product={productWithoutDescription} />);

      expect(screen.queryByText('Salsa de soja japonesa de alta calidad')).not.toBeInTheDocument();
    });
  });

  describe('Stock status', () => {
    it('shows "Agotado" badge when stock is 0', () => {
      const outOfStockProduct = { ...mockProduct, stock: 0 };
      const { container } = renderWithRouter(<ProductCard product={outOfStockProduct} />);

      const badge = container.querySelector('.product-card-badge-out');
      expect(badge).toBeInTheDocument();
      expect(badge).toHaveTextContent('Agotado');
    });

    it('shows "Últimas unidades" badge when stock is low (<=10)', () => {
      const lowStockProduct = { ...mockProduct, stock: 5 };
      const { container } = renderWithRouter(<ProductCard product={lowStockProduct} />);

      const badge = container.querySelector('.product-card-badge-low');
      expect(badge).toBeInTheDocument();
      expect(badge).toHaveTextContent('¡Últimas unidades!');
    });

    it('does not show badges when stock is normal (>10)', () => {
      const { container } = renderWithRouter(<ProductCard product={mockProduct} />);

      const outBadge = container.querySelector('.product-card-badge-out');
      const lowBadge = container.querySelector('.product-card-badge-low');
      expect(outBadge).not.toBeInTheDocument();
      expect(lowBadge).not.toBeInTheDocument();
    });

    it('only shows "Agotado" badge when stock is 0 (not both badges)', () => {
      const outOfStockProduct = { ...mockProduct, stock: 0 };
      const { container } = renderWithRouter(<ProductCard product={outOfStockProduct} />);

      const outBadge = container.querySelector('.product-card-badge-out');
      const lowBadge = container.querySelector('.product-card-badge-low');
      expect(outBadge).toBeInTheDocument();
      expect(lowBadge).not.toBeInTheDocument();
    });
  });

  describe('Add to cart button', () => {
    it('renders "Añadir" button when product is in stock', () => {
      renderWithRouter(<ProductCard product={mockProduct} />);

      const addButton = screen.getByRole('button', { name: /Añadir/i });
      expect(addButton).toBeInTheDocument();
      expect(addButton).not.toBeDisabled();
    });

    it('renders "Agotado" button when stock is 0', () => {
      const outOfStockProduct = { ...mockProduct, stock: 0 };
      renderWithRouter(<ProductCard product={outOfStockProduct} />);

      const button = screen.getByRole('button', { name: /Agotado/i });
      expect(button).toBeInTheDocument();
      expect(button).toBeDisabled();
    });

    it('calls addItem when add to cart button is clicked', async () => {
      mockAddItem.mockResolvedValue({});
      renderWithRouter(<ProductCard product={mockProduct} />);

      const addButton = screen.getByRole('button', { name: /Añadir/i });
      fireEvent.click(addButton);

      await waitFor(() => {
        expect(mockAddItem).toHaveBeenCalledWith(1, 1);
      });
    });

    it('disables button and shows loading state while adding to cart', async () => {
      mockAddItem.mockImplementation(() => new Promise(resolve => setTimeout(resolve, 100)));
      renderWithRouter(<ProductCard product={mockProduct} />);

      const addButton = screen.getByRole('button', { name: /Añadir/i });
      fireEvent.click(addButton);

      await waitFor(() => {
        expect(addButton).toBeDisabled();
      });
    });

    it('does not add to cart when product is out of stock', async () => {
      const outOfStockProduct = { ...mockProduct, stock: 0 };
      renderWithRouter(<ProductCard product={outOfStockProduct} />);

      const button = screen.getByRole('button', { name: /Agotado/i });
      fireEvent.click(button);

      expect(mockAddItem).not.toHaveBeenCalled();
    });

    it('stops event propagation when add to cart is clicked', async () => {
      mockAddItem.mockResolvedValue({});

      const { container } = renderWithRouter(<ProductCard product={mockProduct} />);

      const addButton = screen.getByRole('button', { name: /Añadir/i });

      // Create a spy on stopPropagation
      const clickEvent = new MouseEvent('click', { bubbles: true });
      const stopPropSpy = vi.spyOn(clickEvent, 'stopPropagation');

      fireEvent(addButton, clickEvent);

      await waitFor(() => {
        expect(mockAddItem).toHaveBeenCalled();
      });

      expect(stopPropSpy).toHaveBeenCalled();
    });
  });

  describe('Error handling', () => {
    it('shows alert and navigates to login on 401 error', async () => {
      const alertSpy = vi.spyOn(window, 'alert').mockImplementation(() => {});
      mockAddItem.mockRejectedValue({
        response: { status: 401 }
      });

      renderWithRouter(<ProductCard product={mockProduct} />);

      const addButton = screen.getByRole('button', { name: /Añadir/i });
      fireEvent.click(addButton);

      await waitFor(() => {
        expect(alertSpy).toHaveBeenCalledWith('Debes iniciar sesión para agregar productos al carrito');
        expect(mockNavigate).toHaveBeenCalledWith('/login');
      });

      alertSpy.mockRestore();
    });

    it('shows error message on add to cart failure', async () => {
      const alertSpy = vi.spyOn(window, 'alert').mockImplementation(() => {});
      mockAddItem.mockRejectedValue({
        response: {
          status: 500,
          data: { detail: 'Error del servidor' }
        }
      });

      renderWithRouter(<ProductCard product={mockProduct} />);

      const addButton = screen.getByRole('button', { name: /Añadir/i });
      fireEvent.click(addButton);

      await waitFor(() => {
        expect(alertSpy).toHaveBeenCalledWith('Error del servidor');
      });

      alertSpy.mockRestore();
    });

    it('shows generic error message when no detail provided', async () => {
      const alertSpy = vi.spyOn(window, 'alert').mockImplementation(() => {});
      mockAddItem.mockRejectedValue({});

      renderWithRouter(<ProductCard product={mockProduct} />);

      const addButton = screen.getByRole('button', { name: /Añadir/i });
      fireEvent.click(addButton);

      await waitFor(() => {
        expect(alertSpy).toHaveBeenCalledWith('Error al agregar al carrito');
      });

      alertSpy.mockRestore();
    });
  });

  describe('Navigation', () => {
    it('navigates to product detail page when card is clicked', () => {
      const { container } = renderWithRouter(<ProductCard product={mockProduct} />);

      const card = container.querySelector('.card');
      fireEvent.click(card);

      expect(mockNavigate).toHaveBeenCalledWith('/products/1');
    });

    it('navigates with correct product ID', () => {
      const product = { ...mockProduct, id: 42 };
      const { container } = renderWithRouter(<ProductCard product={product} />);

      const card = container.querySelector('.card');
      fireEvent.click(card);

      expect(mockNavigate).toHaveBeenCalledWith('/products/42');
    });
  });

  describe('Price formatting', () => {
    it('formats price correctly with 2 decimals', () => {
      renderWithRouter(<ProductCard product={mockProduct} />);

      expect(screen.getByText('4,99 €')).toBeInTheDocument();
    });

    it('formats whole number prices correctly', () => {
      const productWithWholePrice = { ...mockProduct, price: 10 };
      renderWithRouter(<ProductCard product={productWithWholePrice} />);

      expect(screen.getByText('10,00 €')).toBeInTheDocument();
    });

    it('formats prices with cents correctly', () => {
      const productWithCents = { ...mockProduct, price: 15.50 };
      renderWithRouter(<ProductCard product={productWithCents} />);

      expect(screen.getByText('15,50 €')).toBeInTheDocument();
    });
  });

  describe('Accessibility', () => {
    it('has alt text for product image', () => {
      renderWithRouter(<ProductCard product={mockProduct} />);

      const image = screen.getByAltText('Salsa Soja Premium');
      expect(image).toBeInTheDocument();
    });

    it('has accessible button text', () => {
      renderWithRouter(<ProductCard product={mockProduct} />);

      const button = screen.getByRole('button', { name: /Añadir/i });
      expect(button).toBeInTheDocument();
    });

    it('button indicates disabled state for screen readers', () => {
      const outOfStockProduct = { ...mockProduct, stock: 0 };
      renderWithRouter(<ProductCard product={outOfStockProduct} />);

      const button = screen.getByRole('button', { name: /Agotado/i });
      expect(button).toHaveAttribute('disabled');
    });
  });
});
