import React from 'react';
import { render, screen, cleanup } from '@testing-library/react';
import { App } from './App';
import { act } from 'react-dom/test-utils';

describe('App', () => {
  afterEach(() => {
    cleanup()
  })

  describe('renders the create account form', () => {
    [
      "First name",
      "Last name",
      "Business email address",
      "Create password",
      "Confirm password",
      "Business email address"
    ].forEach((placeHolder) => {
      it(`renders input with placeholder: [${placeHolder}]`, () => {
        act(() => {
          render(<App />);
        })
  
        const input = screen.getByPlaceholderText(placeHolder);
  
        expect(input).toBeInTheDocument();
      })
    })

    it('renders create account button', () => {
      act(() => {
        render(<App />);
      })

      const createAccountButton = screen.getByText("Create Account");

      expect(createAccountButton).toBeInTheDocument();
    })
  })
})
