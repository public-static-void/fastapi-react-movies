export interface MovieType {
  id: number;
  filename: string;
  name: string | null;
  actors: ActorType[];
  categories: CategoryType[];
  series: SeriesType | null;
  series_number: number | null;
  studio: StudioType | null;
}

export interface MovieFileType {
  id: number;
  filename: string;
}

export interface ActorType {
  id: number;
  name: string;
}

export interface CategoryType {
  id: number;
  name: string;
}

export interface SeriesType {
  id: number;
  name: string;
}

export interface StudioType {
  id: number;
  name: string;
}

export interface HTTPExceptionType {
  detail: MessageType;
}

export interface MessageType {
  message: string;
}

export interface MovieUpdateType {
  name: string | null;
  series_id: number | null;
  series_number: number | null;
  studio_id: number | null;
}
