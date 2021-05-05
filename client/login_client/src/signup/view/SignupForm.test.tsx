import React from 'react';
import { combineReducers, createStore, Store, Action } from 'redux';
import { Provider } from 'react-redux';
import { render, screen, cleanup, fireEvent } from '@testing-library/react';
import { SignupFormComponent } from './signup_form';
import { act } from 'react-dom/test-utils';

import { SignupFormRequest, signupReducer } from '../core/state';
import type { SignupAppState, SignupAction } from '../core/state';

type TestStoreProducer = (additionalReducers?: {}) => Store<SignupAppState, SignupAction>
const getTestStore: TestStoreProducer = (additionalReducers: {} = {}) => createStore(combineReducers({ ...signupReducer, ...additionalReducers }))

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
                    render(
                        <Provider store={getTestStore()}>
                            <SignupFormComponent />
                        </Provider>
                    );
                })

                const input = screen.getByPlaceholderText(placeHolder);

                expect(input).toBeInTheDocument();
            })
        })

        it('renders create account button', () => {
            act(() => {
                render(
                    <Provider store={getTestStore()}>
                        <SignupFormComponent />
                    </Provider>
                );
            })

            const createAccountButton = screen.getByText("Create Account");

            expect(createAccountButton).toBeInTheDocument();
        })

        it('renders the accept terms checkbox', () => {
            act(() => {
                render(
                    <Provider store={getTestStore()}>
                        <SignupFormComponent />
                    </Provider>
                )
            })

            const acceptTermsCheckbox = screen.getByText("I agree to the Terms and Conditions");

            expect(acceptTermsCheckbox).toBeInTheDocument()
        })
    })

    describe('form submission', () => {
        describe('fully populated form', () => {
            fit('can submit a fully populated form', () => {
                const actions: Action<{}>[] = []
                const testStore = getTestStore({
                    test: (s: {} = {}, a: { type: "TEST_ACTION" }): {} => {
                        actions.push(a)
                        return s
                    }
                })
                act(() => {
                    render(
                        <Provider store={testStore}>
                            <SignupFormComponent />
                        </Provider>
                    )
                })

                const emailInput = screen.getByPlaceholderText("Business email address")
                const password = screen.getByPlaceholderText("Create password")
                const confirmPassword = screen.getByPlaceholderText("Confirm password")
                const firstName = screen.getByPlaceholderText("First name")
                const lastName = screen.getByPlaceholderText("Last name")

                const createAccountButton = screen.getByText("Create Account");

                fireEvent.change(emailInput, { target: { value: "email" } })
                fireEvent.change(firstName, { target: { value: "firstName" } })
                fireEvent.change(lastName, { target: { value: "lastName" } })

                fireEvent.change(password, { target: { value: "password" } })
                fireEvent.change(confirmPassword, { target: { value: "password" } })

                fireEvent.click(createAccountButton)

                // check terms and conditions
                // select licensed?

                const submitActions = actions.filter(({ type }) => type === "[SIGNUP] SUBMIT")
                expect(submitActions).toHaveLength(1)

                const [ submitAction ] = submitActions

                const expectedData: SignupFormRequest = {
                    email: "email",
                    password: "password",
                    confirmationPassword: "password",
                    firstName: "firstName",
                    lastName: "lastName",
                    acceptTerms: true
                }
                expect(submitAction).toEqual({
                    type: "[SIGNUP] SUBMIT",
                    data: expectedData
                })
            })
        })

        describe('empty form is not submitted', () => {
            // act(() => {
            //     render(
            //         <Provider store={getTestStore()}>
            //             <SignupFormComponent />
            //         </Provider>
            //     )
            // })

            // const createAccountButton = screen.getByText("Create Account")

            // createAccountButton.click()

            // expect(mockSignupService.signup).not.toHaveBeenCalled()
        })
    })
})
