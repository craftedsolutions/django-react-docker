import { Action, Dispatch } from "redux";

type actionMaker<T> = (t: T) => Action
type simpleActionMaker = () => Action

const dispatchMaker = (dispatch: Dispatch) => <T>(actionMaker: actionMaker<T>) => (t: T) => dispatch(actionMaker(t))
const simpleDispatchMaker = (dispatch: Dispatch) => (simpleActionMaker: simpleActionMaker) => () => dispatch(simpleActionMaker())

export {
    dispatchMaker,
    simpleDispatchMaker
}