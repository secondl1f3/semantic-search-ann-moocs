import React from "react";
import { Flex, Image, Select } from "@mantine/core";
import Moocmaven from "../assets/logo-no-background.png";
import { Language } from "tabler-icons-react";

const Navbar = ({
  size,
  children,
  langData,
  langLoading,
  langError,
  lang,
  setLang,
}) => {
  return (
    <nav className="me-3">
      <Flex
        mih={50}
        gap="md"
        justify="flex-start"
        align="center"
        direction="row"
        wrap="no-wrap"
      >
        <a rel="noopener" href="https://www.moocmaven.com">
          <Image
            size="xs"
            fit="contain"
            width={200}
            height={80}
            src={Moocmaven}
          />
        </a>
        {children}
        <Select
          data={langData || []}
          value={lang}
          onChange={setLang}
          searchable
          nothingFound="No options"
          icon={<Language size="1rem" />}
        />
      </Flex>
    </nav>
  );
};

export default Navbar;
