import React from 'react'

import { connect } from 'react-redux'
import { Action, Dispatch } from 'redux'

import {
    dispatchMaker,
    simpleDispatchMaker
} from "../../core/redux_support"

import type { SignupFormData, SignupFormState, SignupAppState, SignupFormRequest } from '../core/state'
import {
    updateEmail,
    updateFirstName,
    updateLastName,
    updatePassword,
    showPassword,
    hidePassword,
    updatePasswordConfirmation,
    showPasswordConfirmation,
    hidePasswordConfirmation,
    submitSignup
} from '../core/state'

type textFieldUpdate = (updatedValue: string) => void
type SignupFormDispatch = {
    updateEmail: textFieldUpdate
    updateFirstName: textFieldUpdate
    updateLastName: textFieldUpdate
    updatePassword: textFieldUpdate
    showPassword: () => void,
    hidePassword: () => void,
    updateConfirmPassword: textFieldUpdate
    showConfirmPassword: () => void,
    hideConfirmPassword: () => void,
    // updateAcceptTerms: (updatedValue: boolean) => void
    submit: (formState: SignupFormRequest) => void
}

type signupFormStateAndProps = SignupFormState & SignupFormDispatch;

const inputTextUpdate = (handler: (s: string) => void) => (event: React.ChangeEvent<HTMLInputElement>) => handler(event.target.value)

const passwordType = (viewable: boolean) => {
    if (viewable) {
        return "text"
    } else {
        return "password"
    }
}
const pickUpdateFun = (viewable: boolean, show: () => void, hide: () => void) => {
    if (viewable) {
        return hide
    } else {
        return show
    }
}
const PasswordInput: React.FunctionComponent<{ value: string, viewable: boolean, placeholder: string } & { show: () => void, hide: () => void, update: (s: string) => void }> = ({
    value,
    viewable,
    update,
    show,
    hide,
    placeholder
}) => (
    <>
        <input
            type={passwordType(viewable)}
            placeholder={placeholder}
            value={value}
            onChange={inputTextUpdate(update)}
        >
        </input>
        <button
            onClick={pickUpdateFun(viewable, show, hide)}
        >
            SHOW/HIDE
        </button>
    </>
)

const SignupForm: React.FunctionComponent<signupFormStateAndProps> = ({
    email,
    updateEmail,
    firstName,
    updateFirstName,
    lastName,
    updateLastName,
    password,
    updatePassword,
    showPassword,
    hidePassword,
    confirmationPassword,
    updateConfirmPassword,
    showConfirmPassword,
    hideConfirmPassword,
    acceptTerms,
    submitActive,
    submit
}) => {
    return (
        <div>
            <div className="create-account-form">
                <div className="create-form-title">{"Get started as a user!"}</div>
                <div className="input-row">
                    <input
                        className="first-name"
                        type="text"
                        placeholder="First name"
                        onChange={inputTextUpdate(updateFirstName)}
                    >
                    </input>
                    <input
                        className="last-name"
                        type="text"
                        placeholder="Last name"
                        onChange={inputTextUpdate(updateLastName)}
                    >
                    </input>
                </div>
                <div className="input-row">
                    <input
                        type="text"
                        placeholder="Business email address"
                        value={email.value}
                        onChange={inputTextUpdate(updateEmail)}
                    >
                    </input>
                </div>
                <div className="input-row">
                    <PasswordInput
                        {...password}
                        placeholder={"Create password"}
                        update={updatePassword}
                        show={showPassword}
                        hide={hidePassword}
                    />
                </div>
                <div className="input-row">
                    <PasswordInput
                        {...confirmationPassword}
                        placeholder={"Confirm password"}
                        update={updateConfirmPassword}
                        show={showConfirmPassword}
                        hide={hideConfirmPassword}
                    />
                </div>
                <div className="create-account">
                    <button
                        disabled={submitActive}
                        onClick={() => submit({
                            email: email.value,
                            firstName: firstName.value,
                            lastName: lastName.value,
                            password: password.value,
                            confirmationPassword: confirmationPassword.value,
                            acceptTerms: acceptTerms.value
                        })}
                    >
                        {"Create Account"}
                    </button>
                </div>
            </div>
        </div>
    )
}

type ActionMaker<T> = (t: T) => Action

const mapStateToProps: (appState: SignupAppState) => SignupFormState = ({ signup }) => ({ ...signup })
const mapDispatchToProps = (dispatch: Dispatch): SignupFormDispatch => {
    const makeDispatcher = dispatchMaker(dispatch)
    const simpleMakeDispatcher = simpleDispatchMaker(dispatch)

    return {
        submit: makeDispatcher(submitSignup),
        updateEmail: makeDispatcher(updateEmail),
        updateFirstName: makeDispatcher(updateFirstName),
        updateLastName: makeDispatcher(updateLastName),
        updatePassword: makeDispatcher(updatePassword),
        showPassword: simpleMakeDispatcher(showPassword),
        hidePassword: simpleMakeDispatcher(hidePassword),
        updateConfirmPassword: makeDispatcher(updatePasswordConfirmation),
        showConfirmPassword: simpleMakeDispatcher(showPasswordConfirmation),
        hideConfirmPassword: simpleMakeDispatcher(hidePasswordConfirmation)
        // updateAcceptTerms: () => dispatch({})
    }

}
const SignupFormComponent = connect(
    mapStateToProps,
    mapDispatchToProps
)(SignupForm)

export { SignupFormComponent }