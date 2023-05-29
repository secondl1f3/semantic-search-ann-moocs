import React, { useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button, Center, Flex, InputBase } from "@mantine/core";
import Moocmaven from "../assets/logo-no-background.png";
import { useDispatch } from "react-redux";
import { postSearch } from "../redux/actions/searchActions";
import '../App.css';
import '../assets/AppStyle.css';

const Search = ({ withLogo = true, lang }) => {
  const navigate = useNavigate();
  const [searchValue, setSearchValue] = useState("");
  const dispatch = useDispatch();

  const inputRef = useRef();

  const handleOnSubmit = (e) => {
    e.preventDefault();
    dispatch(postSearch({ searchValue: inputRef.current.value, lang: lang }));
    navigate(`/results/${searchValue}/${lang}`);
  };

  const mainStyle = {
    fontSize: "18px",
    textAlign: 'center',
    padding: '40px 0',
    color: "#333"
  };

  return (
    <Center w={"60%"} mx={"auto"}>
      <form
        style={{ height: "80vh", marginTop: "auto", width: "100%" }}
        onSubmit={handleOnSubmit}
      >
        {withLogo ? (
          <Flex p={15} justify={{ sm: "center" }}>
            <img src={Moocmaven} alt="" width="300px" />
          </Flex>
        ) : null}

        <div style={mainStyle}>Search across tens of thousands courses</div>

        <InputBase
          radius="xl"
          size="lg"
          placeholder="Search"
          ref={inputRef}
          value={searchValue}
          onChange={(e) => setSearchValue(e.target.value)}
          styles={{
            input: { borderRadius: "xl", boxShadow: "0 0 4px rgba(0, 0, 0, 0.2)" },
            wrapper: { borderRadius: "xl" },
          }}
        />

        <Flex p={15} gap={5} justify={{ sm: "center" }}>
          <Button type="submit" variant="light" radius="xl">
            Search
          </Button>
          {/* <a href="https://www.google.com/doodles" target="_blank"> */}
          <Button variant="light" radius="xl">Feeling Lucky</Button>
          {/* </a> */}
        </Flex>
      </form>
    </Center>
  );
};

export default Search;
