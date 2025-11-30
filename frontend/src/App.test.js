import { render, screen } from '@testing-library/react';
import App from './App';

test('renders chaos.ai title', () => {
  render(<App />);
  const titleElement = screen.getByText(/chaos.ai/i);
  expect(titleElement).toBeInTheDocument();
});

test('renders create game button', () => {
  render(<App />);
  const buttonElement = screen.getByText(/Create New Game/i);
  expect(buttonElement).toBeInTheDocument();
});

test('renders join game button', () => {
  render(<App />);
  const buttonElement = screen.getByText(/Join Game/i);
  expect(buttonElement).toBeInTheDocument();
});

