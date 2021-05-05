import { combineReducers, createStore, Store } from 'redux'

import { signupReducer } from '../signup/core/state'
import type { SignupAction, SignupAppState } from '../signup/core/state'

type AppState = SignupAppState;
type AppActions = SignupAction;

const combinedReducers = combineReducers({
    ...signupReducer
})

const getStore = (): Store<AppState, AppActions> => createStore(combinedReducers)

export { getStore }