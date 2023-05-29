import axios from "axios";

export const POST_SEARCH = "POST_SEARCH";
export const GET_LANG = "GET_LANG";

const timeout = 120000; //milisec

export const postSearch = ({ searchValue, lang }) => {
  const url = `https://api.moocmaven.com/search`;
  const body = {
    query: searchValue,
    lang: lang || "arabic",
    skip: 0,
    limit: 10,
  };
  return (dispatch) => {
    dispatch({
      type: POST_SEARCH,
      response: {
        loading: true,
        data: false,
        error: false,
      },
    });

    axios({
      method: "POST",
      url: url,
      data: body,
      timeout: timeout,
    })
      .then((response) => {
        dispatch({
          type: POST_SEARCH,
          response: {
            loading: false,
            data: response.data.results,
            error: false,
          },
        });
      })
      .catch((err) => {
        dispatch({
          type: POST_SEARCH,
          response: {
            loading: false,
            data: false,
            error: err.message,
          },
        });
      });
  };
};

export const getLang = () => {
  const url = `https://api.moocmaven.com/languages`;
  return (dispatch) => {
    dispatch({
      type: GET_LANG,
      response: {
        loading: true,
        data: false,
        error: false,
      },
    });

    axios({
      method: "GET",
      url: url,
      timeout: timeout,
    })
      .then((response) => {
        dispatch({
          type: GET_LANG,
          response: {
            loading: false,
            data: response.data.languages,
            error: false,
          },
        });
      })
      .catch((err) => {
        dispatch({
          type: GET_LANG,
          response: {
            loading: false,
            data: false,
            error: err.message,
          },
        });
      });
  };
};
