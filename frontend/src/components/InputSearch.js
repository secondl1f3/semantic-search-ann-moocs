import { TextInput, ActionIcon } from "@mantine/core";
import { Search } from "tabler-icons-react";

export function InputSearch(props) {
  return (
    <>
      <TextInput
        style={{ width: "70%" }}
        radius="xl"
        size="md"
        rightSection={
          <ActionIcon size={32} radius="xl">
            <Search
              size={20}
              strokeWidth={2}
              onClick={(e) => props.onSubmit(e)}
            />
          </ActionIcon>
        }
        value={props.value}
        placeholder="Search"
        rightSectionWidth={42}
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            props.onSubmit(e);
          }
        }}
        {...props}
      />
    </>
  );
}
