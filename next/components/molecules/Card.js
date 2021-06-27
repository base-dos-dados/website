import { Center, Box, VStack, HStack } from "@chakra-ui/react";

export function Card({
  children,
  icons = [],
  spacing = 5,
  padding = "30px 30px 30px 30px",
}) {
  return (
    <Box
      cursor="pointer"
      width="100%"
      minWidth="330px"
      borderRadius="10px"
      filter="drop-shadow(0px 4px 4px rgba(0, 0, 0, 0.25))"
    >
      <VStack
        alignItems="flex-start"
        spacing={spacing}
        backgroundColor="#FFFFFF"
        padding={padding}
        borderRadius="10px"
        position="relative"
      >
        <HStack paddingBottom="20px">{icons}</HStack>
        {children}
      </VStack>
    </Box>
  );
}
