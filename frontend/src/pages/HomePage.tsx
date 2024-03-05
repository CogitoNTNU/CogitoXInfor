import { useCallback, useEffect, useState } from "react";
import { Product } from "../types";
import { GetProducts } from "../services/GetProducts";
import ProductCardGrid from "../components/ProductCardGrid";
import { effect, signal } from "@preact/signals-react";
import debounce from "lodash/debounce";
import { FormControl, InputAdornment, TextField } from "@mui/material";

const currentSearch = signal<string>(sessionStorage.getItem("search") || "");
const page = signal<number>(0);
const rowsPerPage = signal<number>(20);

const HomePage = () => {
  const [products, setProducts] = useState<Product[] | null>(null);
  const [searchValue, setSearchValue] = useState(
    currentSearch.value ? currentSearch.value : ""
  );

  useEffect(() => {
    // get products
    console.log("search", currentSearch.value);

    GetProducts({
      amount: rowsPerPage.value,
      search: currentSearch.value,
      offset: page.value * rowsPerPage.value,
    }).then((products) => {
      if (products) {
        setProducts(products);
      }
    });
  }, [currentSearch.value, page.value, rowsPerPage.value]);

  const debouncedOnSearch = useCallback(
    debounce((searchString: string) => {
      page.value = 0;
      currentSearch.value = searchString;
      sessionStorage.setItem("search", searchString);
    }, 800),
    []
  );

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
    const value = event.target.value;
    debouncedOnSearch(value); // This will trigger the debouncedOnSearch callback after 800ms
    setSearchValue(value);
    if (value === "") {
      page.value = 0;
    }
  };

  const handleKeyDown = (event: React.KeyboardEvent): void => {
    if (event.key === "Enter") {
      page.value = 0;
      currentSearch.value = searchValue;
      sessionStorage.setItem("search", searchValue);
    }
  };

  const handleClick = (): void => {
    setSearchValue("");
    currentSearch.value = "";
    sessionStorage.setItem("search", "");
    page.value = 0;
  };

  return (
    <div className=" gap-4">
      <div className="SearchbarContainer gap-4 m-3">
        <FormControl fullWidth>
          <TextField
            value={searchValue}
            variant="outlined"
            onChange={handleChange}
            onKeyDown={handleKeyDown}
            placeholder="Search for any product..."
            sx={{
              "& .MuiOutlinedInput-root": {
                borderWidth: "4px",
                borderRadius: "30px",
                "&.Mui-focused fieldset": {
                  borderWidth: "4px",
                },
              },
            }}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  {/* <SearchIcon /> */}
                </InputAdornment>
              ),
              endAdornment: (
                <InputAdornment position="end" onClick={handleClick}>
                  {/* <ClearIcon
                    style={{
                      cursor: "pointer",
                      opacity: searchValue ? 1 : 0,
                    }}
                  /> */}
                </InputAdornment>
              ),
            }}
          />
        </FormControl>
      </div>
      <ProductCardGrid products={products || []} />
    </div>
  );
};

export default HomePage;
