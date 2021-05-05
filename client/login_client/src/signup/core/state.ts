import { Dispatch } from "redux"

enum FormStatus {
    SUBMISSION_PENDING,
    COLLECTING_DATA
}

type TextInput = {
    value: string
}
type PasswordInput = {
    value: string
    viewable: boolean
}
type CheckboxInput = {
    value: boolean
}

type SignupFormData = {
    email: TextInput
    firstName: TextInput
    lastName: TextInput
    password: PasswordInput
    confirmationPassword: PasswordInput
    acceptTerms: CheckboxInput
}

type FormType = TextInput | PasswordInput | CheckboxInput;
type SubType<T extends FormType> = T extends TextInput ? string : T extends PasswordInput ? string : T extends CheckboxInput ? boolean : never;
type FormRequest<T extends { [key: string]: FormType }> = {
    [K in keyof T]: SubType<T[K]>
}
type SignupFormRequest = FormRequest<SignupFormData>

type SignupFormState = SignupFormData & {
    submitActive: boolean
    status: FormStatus
}
type SignupAppState = { signup: SignupFormState }

type SignupActionOf<T, D> = {
    type: T
    data: D
}
type SimpleSignupActionOf<T> = {
    type: T
}

enum SignupActionTypes {
    UPDATE_EMAIL = "[SIGNUP] UPDATE_EMAIL",
    UPDATE_FIRST_NAME = "[SIGNUP] UPDATE_FIRST_NAME",
    UPDATE_LAST_NAME = "[SIGNUP] UPDATE_LAST_NAME",
    UPDATE_PASSWORD = "[SIGNUP] UPDATE_PASSWORD",
    SHOW_PASSWORD = "[SIGNUP] SHOW_PASSWORD",
    HIDE_PASSWORD = "[SIGNUP] HIDE_PASSWORD",
    UPDATE_PASSWORD_CONFIRMATION = "[SIGNUP] UPDATE_PASSWORD_CONFIRMATION",
    SHOW_PASSWORD_CONFIRMATION = "[SIGNUP] SHOW_PASSWORD_CONFIRMATION",
    HIDE_PASSWORD_CONFIRMATION = "[SIGNUP] HIDE_PASSWORD_CONFIRMATION",
    SUBMIT = "[SIGNUP] SUBMIT"
}

type UpdateEmail = SignupActionOf<SignupActionTypes.UPDATE_EMAIL, string>
const updateEmail = (data: string): UpdateEmail => ({
    type: SignupActionTypes.UPDATE_EMAIL,
    data
})

type UpdateFirstName = SignupActionOf<SignupActionTypes.UPDATE_FIRST_NAME, string>
const updateFirstName = (data: string): UpdateFirstName => ({
    type: SignupActionTypes.UPDATE_FIRST_NAME,
    data
})
type UpdateLastName = SignupActionOf<SignupActionTypes.UPDATE_LAST_NAME, string>
const updateLastName = (data: string): UpdateLastName => ({
    type: SignupActionTypes.UPDATE_LAST_NAME,
    data
})

type UpdatePassword = SignupActionOf<SignupActionTypes.UPDATE_PASSWORD, string>
const updatePassword = (data: string): UpdatePassword => ({
    type: SignupActionTypes.UPDATE_PASSWORD,
    data
})
type ShowPassword = SimpleSignupActionOf<SignupActionTypes.SHOW_PASSWORD>
const showPassword = (): ShowPassword => ({ type: SignupActionTypes.SHOW_PASSWORD })
type HidePassword = SimpleSignupActionOf<SignupActionTypes.HIDE_PASSWORD>
const hidePassword = (): HidePassword => ({ type: SignupActionTypes.HIDE_PASSWORD })

type UpdatePasswordConfirmation = SignupActionOf<SignupActionTypes.UPDATE_PASSWORD_CONFIRMATION, string>
const updatePasswordConfirmation = (data: string): UpdatePasswordConfirmation => ({
    type: SignupActionTypes.UPDATE_PASSWORD_CONFIRMATION,
    data
})
type ShowPasswordConfirmation = SimpleSignupActionOf<SignupActionTypes.SHOW_PASSWORD_CONFIRMATION>
const showPasswordConfirmation = (): ShowPasswordConfirmation => ({ type: SignupActionTypes.SHOW_PASSWORD_CONFIRMATION })
type HidePasswordConfirmation = SimpleSignupActionOf<SignupActionTypes.HIDE_PASSWORD_CONFIRMATION>
const hidePasswordConfirmation = (): HidePasswordConfirmation => ({ type: SignupActionTypes.HIDE_PASSWORD_CONFIRMATION })

type SubmitSignup = SignupActionOf<SignupActionTypes.SUBMIT, SignupFormRequest>
const submitSignup = (data: SignupFormRequest): SubmitSignup => ({
    type: SignupActionTypes.SUBMIT,
    data
})

type SignupAction = UpdateEmail
    | UpdateFirstName
    | UpdateLastName
    | UpdatePassword
    | ShowPassword
    | HidePassword
    | UpdatePasswordConfirmation
    | ShowPasswordConfirmation
    | HidePasswordConfirmation
    | SubmitSignup;

type ExternalReducer<ES, S, A> = { [key in keyof ES]: (state: S, action: A) => S }

const initialState: SignupFormState = {
    email: { value: "" },
    firstName: { value: "" },
    lastName: { value: "" },
    password: { value: "", viewable: false },
    confirmationPassword: { value: "", viewable: false },
    acceptTerms: { value: false },
    submitActive: false,
    status: FormStatus.COLLECTING_DATA
}

const fallThrough = (a: never, state: SignupFormState): SignupFormState => state;
const reducer = (state: SignupFormState = initialState, action: SignupAction): SignupFormState => {
    switch (action.type) {
        case SignupActionTypes.UPDATE_EMAIL:
            return {
                ...state,
                email: { value: action.data }
            }
        case SignupActionTypes.UPDATE_FIRST_NAME:
            return {
                ...state,
                firstName: { value: action.data }
            }
        case SignupActionTypes.UPDATE_LAST_NAME:
            return {
                ...state,
                lastName: { value: action.data }
            }
        case SignupActionTypes.SUBMIT:
            return {
                ...state,
                status: FormStatus.SUBMISSION_PENDING
            }
        case SignupActionTypes.UPDATE_PASSWORD:
            return {
                ...state,
                password: {
                    value: action.data,
                    viewable: state.password.viewable
                }
            }
        case SignupActionTypes.HIDE_PASSWORD:
            return {
                ...state,
                password: {
                    ...state.password,
                    viewable: false
                }
            }
        case SignupActionTypes.SHOW_PASSWORD:
            return {
                ...state,
                password: {
                    ...state.password,
                    viewable: true
                }
            }
        case SignupActionTypes.UPDATE_PASSWORD_CONFIRMATION:
            console.log("ACTION:", JSON.stringify(action, null, 2))
            return {
                ...state,
                confirmationPassword: {
                    value: action.data,
                    viewable: state.confirmationPassword.viewable
                }
            }
        case SignupActionTypes.HIDE_PASSWORD_CONFIRMATION:
            return {
                ...state,
                confirmationPassword: {
                    ...state.confirmationPassword,
                    viewable: false
                }
            }
        case SignupActionTypes.SHOW_PASSWORD_CONFIRMATION:
            return {
                ...state,
                confirmationPassword: {
                    ...state.confirmationPassword,
                    viewable: true
                }
            }
    }

    return fallThrough(action, state)
}

const signupReducer: ExternalReducer<SignupAppState, SignupFormState, SignupAction> = { signup: reducer }

export {
    signupReducer,
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
}
export type {
    SignupAction,
    SignupAppState,
    SignupFormData,
    SignupFormState,
    SignupFormRequest
}