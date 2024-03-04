export interface Product {
  id: string;
  title: string;
  price: number;
  manufacturer: string;
  description: string;
}

export interface RecommendationFormat {
  id: string;
  amount: number;
}

export interface GetProduct {
  amount: number;
  search: string;
  offset: number;
}
