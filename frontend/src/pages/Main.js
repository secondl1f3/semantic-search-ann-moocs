import React, { useEffect, useState } from "react";
import Search from "../components/Search";
import PageFooter from "../components/PageFooter";
import { Container } from "@mantine/core";
import { useDispatch, useSelector } from "react-redux";
import { getLang } from "../redux/actions/searchActions";

export default function Main() {
  const dispatch = useDispatch();
  const [lang, setLang] = useState("arabic");
  const { getLangLoading, getLangData, getLangError } = useSelector(
    (state) => state.searchReducer
  );
  useEffect(() => {
    dispatch(getLang());
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <Container className="main-container">
      <div className="flex-container">
        <Search lang={lang} />
        {/* <Lang
          langData={getLangData}
          langLoading={getLangLoading}
          langError={getLangError}
          lang={lang}
          setLang={setLang}
        /> */}
      </div>
      <PageFooter></PageFooter>
    </Container>
  );
}
