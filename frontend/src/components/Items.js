import React from "react";
import { List, Anchor, Text } from "@mantine/core";

const Items = ({ data = [] }) => {
  return (
    <>
      {data ? (
        data.map((item, index) => {
          return (
            <List.Item key={`item-${index}`}>
              <div>
                <Anchor href={item.url} target="_blank">
                  {item.title}
                </Anchor>
                <div>
                  <Text c="dimmed" lineClamp={2}>
                    {item.description}
                  </Text>
                </div>
                <div>
                  <Text fw={500}>{item.instructor}</Text>
                </div>
              </div>
            </List.Item>
          );
        })
      ) : (
        <div>no data found</div>
      )}
    </>
  );
};

export default Items;
