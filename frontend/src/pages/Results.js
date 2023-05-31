import React, { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import { Alert, Container } from "@mantine/core";
import { InputSearch } from "../components/InputSearch";
import ContentItems from "../components/ContentsItems";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate, useParams } from "react-router-dom";
import { getLang, postSearch } from "../redux/actions/searchActions";
import { AlertCircle } from "tabler-icons-react";

const Results = () => {
  const dispatch = useDispatch();
  const params = useParams();
  const navigate = useNavigate();

  const searchPropsValue = params ? params.searchValue : null;
  const searchPropsLang = params ? params.lang : null;

  const [searchValue, setSearchValue] = useState(searchPropsValue);
  const [searchLang, setSearchLang] = useState(searchPropsLang);
  const [showError, setShowError] = useState(false);
  const { postSearchLoading, postSearchData, postSearchError } = useSelector(
    (state) => state.searchReducer
  );

  const { getLangLoading, getLangData, getLangError } = useSelector(
    (state) => state.searchReducer
  );

  useEffect(() => {
    if (!getLangData) {
      dispatch(getLang());
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (!postSearchLoading) {
      if (!postSearchData && searchValue !== null) {
        dispatch(postSearch({ searchValue: searchValue, lang: searchLang }));
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (!postSearchLoading && postSearchError) {
      setShowError(true);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [postSearchLoading]);

  const handleOnSubmit = (e) => {
    e.preventDefault();
    dispatch(postSearch({ searchValue: searchValue, lang: searchLang }));
    navigate(`/results/${searchValue}/${searchLang}`);
  };

  const handleOnChange = (e) => {
    setSearchValue(e.target.value);
  };

  // if (postSearchError) return <>{postSearchError}</>;

  return (
    <Container size={"lg"}>
      <Navbar
        langData={getLangData}
        langLoading={getLangLoading}
        langError={getLangError}
        lang={searchLang}
        setLang={setSearchLang}
      >
        <InputSearch
          value={searchValue}
          // lang={searchLang}
          onChange={handleOnChange}
          onSubmit={handleOnSubmit}
        />
      </Navbar>
      <Container style={{ paddingLeft: "10%" }} size="md" px="xs">
        {!postSearchError ? (
          <ContentItems
            data={postSearchData}
            loading={postSearchLoading}
            // error={postSearchError}
          />
        ) : showError ? (
          <Alert
            withCloseButton
            icon={<AlertCircle size="1rem" />}
            title={postSearchError}
            color="red"
            onClose={(e) => {
              setShowError(false);
            }}
          >
            {postSearchError}
          </Alert>
        ) : null}
      </Container>
    </Container>
  );
};

export default Results;
