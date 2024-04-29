export interface Product {
  id: string;
  title: string;
  price: number;
  manufacturer: string;
  description: string;
  picture: string;
}

export interface RecommendationFormat {
  id: string;
  amount: number;
}

export interface GetProducts {
  amount: number;
  search: string;
  offset: number;
}

export interface GetProduct {
  id: string;
}
