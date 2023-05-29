import { POST_SEARCH, GET_LANG } from "../../actions/searchActions";

const initialState = {
  postSearchLoading: false,
  postSearchData: false,
  postSearchError: false,

  getLangLoading: false,
  getLangData: false,
  getLangError: false,
};

const search = (state = initialState, action) => {
  switch (action.type) {
    case POST_SEARCH:
      return {
        ...state,
        postSearchLoading: action.response.loading,
        postSearchData: action.response.data,
        postSearchError: action.response.error,
      };
    case GET_LANG:
      return {
        ...state,
        getLangLoading: action.response.loading,
        getLangData: action.response.data,
        getLangError: action.response.error,
      };
    default:
      return state;
  }
};

export default search;
