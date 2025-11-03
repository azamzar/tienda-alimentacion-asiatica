import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/react';
import Skeleton from '../../../components/common/Skeleton';

describe('Skeleton', () => {
  describe('Basic rendering', () => {
    it('renders with default props', () => {
      const { container } = render(<Skeleton />);
      const skeleton = container.querySelector('.skeleton');

      expect(skeleton).toBeInTheDocument();
      expect(skeleton).toHaveClass('skeleton--text');
      expect(skeleton).toHaveClass('skeleton--animated');
    });

    it('renders with custom className', () => {
      const { container } = render(<Skeleton className="custom-skeleton" />);
      const skeleton = container.querySelector('.skeleton');

      expect(skeleton).toHaveClass('custom-skeleton');
    });
  });

  describe('Variants', () => {
    it('renders text variant', () => {
      const { container } = render(<Skeleton variant="text" />);
      const skeleton = container.querySelector('.skeleton');

      expect(skeleton).toHaveClass('skeleton--text');
    });

    it('renders circular variant', () => {
      const { container } = render(<Skeleton variant="circular" />);
      const skeleton = container.querySelector('.skeleton');

      expect(skeleton).toHaveClass('skeleton--circular');
    });

    it('renders rectangular variant', () => {
      const { container } = render(<Skeleton variant="rectangular" />);
      const skeleton = container.querySelector('.skeleton');

      expect(skeleton).toHaveClass('skeleton--rectangular');
    });
  });

  describe('Dimensions', () => {
    it('applies width prop', () => {
      const { container } = render(<Skeleton width="200px" />);
      const skeleton = container.querySelector('.skeleton');

      expect(skeleton).toHaveStyle({ width: '200px' });
    });

    it('applies height prop for non-text variants', () => {
      const { container } = render(<Skeleton variant="rectangular" height="100px" />);
      const skeleton = container.querySelector('.skeleton');

      expect(skeleton).toHaveStyle({ height: '100px' });
    });

    it('uses default width of 100%', () => {
      const { container } = render(<Skeleton />);
      const skeleton = container.querySelector('.skeleton');

      expect(skeleton).toHaveStyle({ width: '100%' });
    });

    it('uses 1em height for text variant', () => {
      const { container } = render(<Skeleton variant="text" height="100px" />);
      const skeleton = container.querySelector('.skeleton');

      // Text variant should override height to 1em
      expect(skeleton).toHaveStyle({ height: '1em' });
    });

    it('applies custom height for non-text variants', () => {
      const { container } = render(
        <Skeleton variant="rectangular" width="300px" height="150px" />
      );
      const skeleton = container.querySelector('.skeleton');

      expect(skeleton).toHaveStyle({ width: '300px', height: '150px' });
    });
  });

  describe('Animation', () => {
    it('shows animation by default', () => {
      const { container } = render(<Skeleton />);
      const skeleton = container.querySelector('.skeleton');

      expect(skeleton).toHaveClass('skeleton--animated');
    });

    it('shows animation when animation=true', () => {
      const { container } = render(<Skeleton animation={true} />);
      const skeleton = container.querySelector('.skeleton');

      expect(skeleton).toHaveClass('skeleton--animated');
    });

    it('hides animation when animation=false', () => {
      const { container } = render(<Skeleton animation={false} />);
      const skeleton = container.querySelector('.skeleton');

      expect(skeleton).not.toHaveClass('skeleton--animated');
    });
  });

  describe('Combined props', () => {
    it('renders with all custom props', () => {
      const { container } = render(
        <Skeleton
          variant="circular"
          width="50px"
          height="50px"
          className="avatar-skeleton"
          animation={false}
        />
      );
      const skeleton = container.querySelector('.skeleton');

      expect(skeleton).toHaveClass('skeleton--circular');
      expect(skeleton).toHaveClass('avatar-skeleton');
      expect(skeleton).not.toHaveClass('skeleton--animated');
      expect(skeleton).toHaveStyle({ width: '50px', height: '50px' });
    });

    it('renders with percentage dimensions', () => {
      const { container } = render(
        <Skeleton variant="rectangular" width="80%" height="100%" />
      );
      const skeleton = container.querySelector('.skeleton');

      expect(skeleton).toHaveStyle({ width: '80%', height: '100%' });
    });
  });
});
