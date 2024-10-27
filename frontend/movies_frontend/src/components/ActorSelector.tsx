import ActorSelectorList from './ActorSelectorList';
import Loading from './Loading';
import MovieSection from './MovieSection';
import {
  useActorsQuery,
  useMovieActorAddMutation,
  useMovieActorDeleteMutation,
  useMovieQuery,
} from '../state/MovieManagerApi';
import { FetchBaseQueryError, skipToken } from '@reduxjs/toolkit/query';
import { MainPageFormValuesType } from '../types/form';
import { HTTPExceptionType, MovieType } from '../types/api';
import { setAvailableId, setSelectedId } from '../state/SelectBoxSlice';
import { useAppDispatch, useAppSelector } from '../state/hooks';
import { useFormikContext } from 'formik';

const ActorSelector = () => {
  const formik = useFormikContext<MainPageFormValuesType>();
  const dispatch = useAppDispatch();
  const [movieActorAddTrigger] = useMovieActorAddMutation();
  const [movieActorDeleteTrigger] = useMovieActorDeleteMutation();
  const { availableId, selectedId, movieId } = useAppSelector(
    (state) => state.selectBox
  );
  const { data: actorsAvailable, isLoading } = useActorsQuery();
  const { data: movie } = useMovieQuery(movieId ? movieId : skipToken);

  const onUpdateActor = async (selected: boolean) => {
    if (movieId) {
      const actorId = selected ? availableId : selectedId;
      const trigger = selected ? movieActorAddTrigger : movieActorDeleteTrigger;
      const actorName = actorsAvailable?.find(
        (actor) => actor.id === +actorId!
      )?.name;
      try {
        const data: MovieType = await trigger({
          actorId: actorId!,
          movieId: movieId,
        }).unwrap();
        formik.setStatus(
          `Successfully ${selected ? 'added' : 'removed'} ${actorName} ${
            selected ? 'to' : 'from'
          } ${data.name}`
        );
      } catch (error) {
        const { status, data } = error as FetchBaseQueryError;
        if (status != 422) {
          const {
            detail: { message },
          } = data as HTTPExceptionType;
          formik.setStatus(message ? message : 'Unknown server error');
        }
      }
    }
  };

  return (
    <MovieSection title="Actors">
      <fieldset disabled={!movieId}>
        <div className="flex h-72">
          {isLoading ? (
            <div className="w-full">
              <Loading />
            </div>
          ) : (
            <ActorSelectorList name="actorsAvailable" title="Available">
              <select
                className="border border-solid border-green-500 w-full"
                id="actorsAvailable"
                size={10}
                defaultValue={availableId}
                onChange={(e) => dispatch(setAvailableId(e.target.value))}
                onDoubleClick={() => void onUpdateActor(true)}
                onKeyDown={(e) => {
                  if (e.code === 'Enter') {
                    void onUpdateActor(true);
                  }
                }}
              >
                {actorsAvailable?.map((actor) => (
                  <option
                    key={actor.id}
                    value={actor.id}
                    data-testid={`actors-available-${actor.id}`}
                  >
                    {actor.name}
                  </option>
                ))}
              </select>
            </ActorSelectorList>
          )}
          <ActorSelectorList name="actorsSelected" title="Selected">
            {movieId && movie?.actors && movie.actors.length > 0 ? (
              <select
                className="border border-solid border-green-500 w-full"
                id="actorsSelected"
                size={10}
                defaultValue={selectedId}
                onChange={(e) => dispatch(setSelectedId(e.target.value))}
                onDoubleClick={() => {
                  if (selectedId) {
                    void onUpdateActor(false);
                  }
                }}
                onKeyDown={(e) => {
                  if (e.code === 'Enter' && selectedId) {
                    void onUpdateActor(false);
                  }
                }}
              >
                {movie?.actors.map((actor) => (
                  <option
                    key={actor.id}
                    value={actor.id}
                    data-testid={`actors-selected-${actor.id}`}
                  >
                    {actor.name}
                  </option>
                ))}
              </select>
            ) : (
              <div className="border border-solid border-green-500">
                <h3 className="text-center text-lg font-bold">None</h3>
              </div>
            )}
          </ActorSelectorList>
        </div>
      </fieldset>
    </MovieSection>
  );
};

export default ActorSelector;
