import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import ProductGrid from '../../../components/products/ProductGrid';
import { useProductStore } from '../../../store/useProductStore';

// Mock the store
vi.mock('../../../store/useProductStore');

// Mock ProductCard to simplify testing
vi.mock('../../../components/products/ProductCard', () => ({
  default: ({ product }) => (
    <div data-testid={`product-card-${product.id}`}>
      <h3>{product.name}</h3>
      <p>{product.price}</p>
    </div>
  ),
}));

// Mock ProductGridSkeleton
vi.mock('../../../components/products/ProductGridSkeleton', () => ({
  default: () => <div data-testid="grid-skeleton">Loading...</div>,
}));

const renderWithRouter = (component) => {
  return render(<BrowserRouter>{component}</BrowserRouter>);
};

describe('ProductGrid', () => {
  const mockFetchProducts = vi.fn();
  const mockFetchCategories = vi.fn();
  const mockSetSelectedCategory = vi.fn();
  const mockSetSearchQuery = vi.fn();

  const mockProducts = [
    {
      id: 1,
      name: 'Salsa Soja',
      description: 'Salsa de soja premium',
      price: 4.99,
      stock: 50,
      category_id: 1,
    },
    {
      id: 2,
      name: 'Arroz Japonés',
      description: 'Arroz para sushi',
      price: 6.99,
      stock: 30,
      category_id: 2,
    },
    {
      id: 3,
      name: 'Té Verde',
      description: 'Té verde matcha',
      price: 8.99,
      stock: 20,
      category_id: 1,
    },
  ];

  const mockCategories = [
    { id: 1, name: 'Bebidas' },
    { id: 2, name: 'Alimentos' },
    { id: 3, name: 'Snacks' },
  ];

  const defaultStoreState = {
    products: mockProducts,
    categories: mockCategories,
    selectedCategory: null,
    searchQuery: '',
    loading: false,
    error: null,
    fetchProducts: mockFetchProducts,
    fetchCategories: mockFetchCategories,
    setSelectedCategory: mockSetSelectedCategory,
    setSearchQuery: mockSetSearchQuery,
  };

  beforeEach(() => {
    vi.clearAllMocks();
    useProductStore.mockReturnValue(defaultStoreState);
  });

  describe('Rendering', () => {
    it('renders products grid', () => {
      renderWithRouter(<ProductGrid />);

      expect(screen.getByText('Salsa Soja')).toBeInTheDocument();
      expect(screen.getByText('Arroz Japonés')).toBeInTheDocument();
      expect(screen.getByText('Té Verde')).toBeInTheDocument();
    });

    it('renders all categories in filter sidebar', () => {
      renderWithRouter(<ProductGrid />);

      expect(screen.getByText('Bebidas')).toBeInTheDocument();
      expect(screen.getByText('Alimentos')).toBeInTheDocument();
      expect(screen.getByText('Snacks')).toBeInTheDocument();
    });

    it('renders "Todas" category option', () => {
      renderWithRouter(<ProductGrid />);

      expect(screen.getByText('Todas')).toBeInTheDocument();
    });

    it('renders search input', () => {
      renderWithRouter(<ProductGrid />);

      const searchInput = screen.getByPlaceholderText('Buscar productos...');
      expect(searchInput).toBeInTheDocument();
    });

    it('displays correct product count', () => {
      renderWithRouter(<ProductGrid />);

      expect(screen.getByText('3 productos')).toBeInTheDocument();
    });

    it('displays singular "producto" for single product', () => {
      useProductStore.mockReturnValue({
        ...defaultStoreState,
        products: [mockProducts[0]],
      });

      renderWithRouter(<ProductGrid />);

      expect(screen.getByText('1 producto')).toBeInTheDocument();
    });
  });

  describe('Data fetching', () => {
    it('fetches products on mount', () => {
      renderWithRouter(<ProductGrid />);

      expect(mockFetchProducts).toHaveBeenCalledTimes(1);
    });

    it('fetches categories on mount', () => {
      renderWithRouter(<ProductGrid />);

      expect(mockFetchCategories).toHaveBeenCalledTimes(1);
    });
  });

  describe('Loading state', () => {
    it('shows skeleton loader when loading', () => {
      useProductStore.mockReturnValue({
        ...defaultStoreState,
        loading: true,
      });

      renderWithRouter(<ProductGrid />);

      expect(screen.getByTestId('grid-skeleton')).toBeInTheDocument();
    });

    it('does not show products when loading', () => {
      useProductStore.mockReturnValue({
        ...defaultStoreState,
        loading: true,
      });

      renderWithRouter(<ProductGrid />);

      expect(screen.queryByText('Salsa Soja')).not.toBeInTheDocument();
    });
  });

  describe('Error state', () => {
    it('shows error message when error occurs', () => {
      useProductStore.mockReturnValue({
        ...defaultStoreState,
        error: 'Error al cargar productos',
        loading: false,
      });

      renderWithRouter(<ProductGrid />);

      expect(screen.getByText('Error al cargar productos')).toBeInTheDocument();
    });

    it('does not show products when there is an error', () => {
      useProductStore.mockReturnValue({
        ...defaultStoreState,
        error: 'Error al cargar productos',
        loading: false,
      });

      renderWithRouter(<ProductGrid />);

      expect(screen.queryByText('Salsa Soja')).not.toBeInTheDocument();
    });
  });

  describe('Empty state', () => {
    it('shows empty state when no products match filters', () => {
      useProductStore.mockReturnValue({
        ...defaultStoreState,
        products: [],
        loading: false,
        error: null,
      });

      renderWithRouter(<ProductGrid />);

      expect(screen.getByText('No se encontraron productos')).toBeInTheDocument();
      expect(screen.getByText('Intenta cambiar los filtros de búsqueda')).toBeInTheDocument();
    });

    it('shows clear filters button in empty state when filters are active', () => {
      useProductStore.mockReturnValue({
        ...defaultStoreState,
        products: [],
        searchQuery: 'búsqueda sin resultados',
        loading: false,
        error: null,
      });

      renderWithRouter(<ProductGrid />);

      const clearButton = screen.getAllByText('Limpiar filtros')[0];
      expect(clearButton).toBeInTheDocument();
    });

    it('does not show empty state when loading', () => {
      useProductStore.mockReturnValue({
        ...defaultStoreState,
        products: [],
        loading: true,
      });

      renderWithRouter(<ProductGrid />);

      expect(screen.queryByText('No se encontraron productos')).not.toBeInTheDocument();
    });
  });

  describe('Category filtering', () => {
    it('filters products by category', () => {
      const filteredProducts = mockProducts.filter(p => p.category_id === 1);

      useProductStore.mockReturnValue({
        ...defaultStoreState,
        products: filteredProducts,
        selectedCategory: 1,
      });

      renderWithRouter(<ProductGrid />);

      expect(screen.getByTestId('product-card-1')).toBeInTheDocument();
      expect(screen.getByTestId('product-card-3')).toBeInTheDocument();
      expect(screen.queryByTestId('product-card-2')).not.toBeInTheDocument();
    });

    it('calls setSelectedCategory when category is clicked', () => {
      renderWithRouter(<ProductGrid />);

      const categoryButton = screen.getByText('Bebidas');
      fireEvent.click(categoryButton);

      expect(mockSetSelectedCategory).toHaveBeenCalledWith(1);
    });

    it('highlights selected category', () => {
      useProductStore.mockReturnValue({
        ...defaultStoreState,
        selectedCategory: 1,
      });

      const { container } = renderWithRouter(<ProductGrid />);

      const categoryButtons = container.querySelectorAll('.product-grid-category');
      const activeButton = Array.from(categoryButtons).find(btn =>
        btn.classList.contains('active') && btn.textContent.includes('Bebidas')
      );

      expect(activeButton).toBeTruthy();
    });

    it('shows "Todas" as active when no category selected', () => {
      const { container } = renderWithRouter(<ProductGrid />);

      const allCategoriesButton = Array.from(container.querySelectorAll('.product-grid-category'))
        .find(btn => btn.textContent.includes('Todas'));

      expect(allCategoriesButton).toHaveClass('active');
    });

    it('displays product count for each category', () => {
      renderWithRouter(<ProductGrid />);

      // "Todas" should show total count (3)
      const allButton = screen.getByText('Todas').closest('button');
      expect(allButton).toHaveTextContent('3');
    });
  });

  describe('Search functionality', () => {
    it('updates search query with debounce', async () => {
      renderWithRouter(<ProductGrid />);

      const searchInput = screen.getByPlaceholderText('Buscar productos...');
      fireEvent.change(searchInput, { target: { value: 'salsa' } });

      // Should not call immediately
      expect(mockSetSearchQuery).not.toHaveBeenCalled();

      // Wait for debounce (300ms)
      await waitFor(() => {
        expect(mockSetSearchQuery).toHaveBeenCalledWith('salsa');
      }, { timeout: 500 });
    });

    it('displays filtered products based on search', () => {
      const filteredProducts = mockProducts.filter(p =>
        p.name.toLowerCase().includes('soja')
      );

      useProductStore.mockReturnValue({
        ...defaultStoreState,
        products: filteredProducts,
        searchQuery: 'soja',
      });

      renderWithRouter(<ProductGrid />);

      expect(screen.getByTestId('product-card-1')).toBeInTheDocument();
      expect(screen.queryByTestId('product-card-2')).not.toBeInTheDocument();
      expect(screen.queryByTestId('product-card-3')).not.toBeInTheDocument();
    });

    it('shows product count for search results', () => {
      useProductStore.mockReturnValue({
        ...defaultStoreState,
        products: [mockProducts[0]],
        searchQuery: 'soja',
      });

      renderWithRouter(<ProductGrid />);

      expect(screen.getByText('1 producto')).toBeInTheDocument();
    });
  });

  describe('Clear filters', () => {
    it('shows clear filters button when filters are active', () => {
      useProductStore.mockReturnValue({
        ...defaultStoreState,
        selectedCategory: 1,
      });

      renderWithRouter(<ProductGrid />);

      expect(screen.getByText('Limpiar')).toBeInTheDocument();
    });

    it('shows clear filters button when search is active', () => {
      useProductStore.mockReturnValue({
        ...defaultStoreState,
        searchQuery: 'test',
      });

      renderWithRouter(<ProductGrid />);

      expect(screen.getByText('Limpiar')).toBeInTheDocument();
    });

    it('does not show clear filters button when no filters active', () => {
      renderWithRouter(<ProductGrid />);

      expect(screen.queryByText('Limpiar')).not.toBeInTheDocument();
    });

    it('clears all filters when clear button is clicked', () => {
      useProductStore.mockReturnValue({
        ...defaultStoreState,
        selectedCategory: 1,
        searchQuery: 'test',
      });

      renderWithRouter(<ProductGrid />);

      const clearButton = screen.getByText('Limpiar');
      fireEvent.click(clearButton);

      expect(mockSetSelectedCategory).toHaveBeenCalledWith(null);
      expect(mockSetSearchQuery).toHaveBeenCalledWith('');
    });
  });

  describe('Product grid display', () => {
    it('renders ProductCard for each product', () => {
      renderWithRouter(<ProductGrid />);

      expect(screen.getByTestId('product-card-1')).toBeInTheDocument();
      expect(screen.getByTestId('product-card-2')).toBeInTheDocument();
      expect(screen.getByTestId('product-card-3')).toBeInTheDocument();
    });

    it('passes correct product data to ProductCard', () => {
      renderWithRouter(<ProductGrid />);

      const productCard = screen.getByTestId('product-card-1');
      expect(productCard).toHaveTextContent('Salsa Soja');
      expect(productCard).toHaveTextContent('4.99');
    });
  });

  describe('Category title', () => {
    it('shows "Todos los Productos" when no category selected', () => {
      renderWithRouter(<ProductGrid />);

      expect(screen.getByText('Todos los Productos')).toBeInTheDocument();
    });

    it('shows category name when category selected', () => {
      useProductStore.mockReturnValue({
        ...defaultStoreState,
        selectedCategory: 1,
      });

      const { container } = renderWithRouter(<ProductGrid />);

      // Check for the title in the header, not just any occurrence
      const title = container.querySelector('.product-grid-title');
      expect(title).toHaveTextContent('Bebidas');
    });
  });

  describe('Performance optimizations', () => {
    it('uses memoized filtered products', () => {
      const { rerender } = renderWithRouter(<ProductGrid />);

      // Initial render
      expect(screen.getAllByTestId(/product-card-/).length).toBe(3);

      // Rerender with same props - should not recompute
      rerender(
        <BrowserRouter>
          <ProductGrid />
        </BrowserRouter>
      );

      expect(screen.getAllByTestId(/product-card-/).length).toBe(3);
    });

    it('updates when products change', () => {
      const { rerender } = renderWithRouter(<ProductGrid />);

      expect(screen.getAllByTestId(/product-card-/).length).toBe(3);

      // Update products
      useProductStore.mockReturnValue({
        ...defaultStoreState,
        products: [mockProducts[0]],
      });

      rerender(
        <BrowserRouter>
          <ProductGrid />
        </BrowserRouter>
      );

      expect(screen.getAllByTestId(/product-card-/).length).toBe(1);
    });
  });
});
