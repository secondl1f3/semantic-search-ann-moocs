import React from "react";
import { Flex, Select } from "@mantine/core";
import { Language } from "tabler-icons-react";

const Lang = ({
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

export default Lang;
