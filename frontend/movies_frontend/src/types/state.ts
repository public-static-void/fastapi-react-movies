import type { MovieUpdateType } from './api';

export interface MovieUpdateQueryType extends MovieUpdateType {
  id: string;
}

export interface MovieActorAssociationtype {
  actorId: string;
  movieId: string;
}

export interface MovieCategoryAssociationtype {
  categoryId: string;
  movieId: string;
}

export interface MoviePropertyType {
  id: string;
  name: string;
}

export interface SelectBoxSliceType {
  availableId: string | null;
  selectedId: string | null;
  movieId: string | null;
}
