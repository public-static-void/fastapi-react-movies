import MoviePropertyFormSelector from './MoviePropertyFormSelector';
import {
  ActorType,
  CategoryType,
  HTTPExceptionType,
  SeriesType,
  StudioType,
} from '../types/api';
import {
  useActorAddMutation,
  useActorDeleteMutation,
  useActorsQuery,
  useActorUpdateMutation,
  useCategoriesQuery,
  useCategoryAddMutation,
  useCategoryDeleteMutation,
  useCategoryUpdateMutation,
  useSeriesAddMutation,
  useSeriesDeleteMutation,
  useSeriesQuery,
  useSeriesUpdateMutation,
  useStudioAddMutation,
  useStudioDeleteMutation,
  useStudiosQuery,
  useStudioUpdateMutation,
} from '../state/MovieManagerApi';
import { FetchBaseQueryError } from '@reduxjs/toolkit/query';
import { Field, Formik, FormikHelpers, useFormikContext } from 'formik';
import { MoviePropertyFormValuesType } from '../types/form';
import { useEffect } from 'react';

const NameSelectorChanged = () => {
  const {
    setFieldValue,
    values: { nameSelection, selection },
  } = useFormikContext<MoviePropertyFormValuesType>();
  const { data: actorsAvailable } = useActorsQuery();
  const { data: categories } = useCategoriesQuery();
  const { data: series } = useSeriesQuery();
  const { data: studios } = useStudiosQuery();

  useEffect(() => {
    const _id = +nameSelection;
    if (_id === 0) {
      void setFieldValue('name', '');
    } else {
      let names: ActorType[] | CategoryType[] | SeriesType[] | StudioType[];
      switch (selection) {
        case 'actor':
          names = actorsAvailable ?? [];
          break;
        case 'category':
          names = categories ?? [];
          break;
        case 'series':
          names = series ?? [];
          break;
        case 'studio':
          names = studios ?? [];
          break;
      }
      const selected_names = names.filter((_name) => _id === _name.id);
      if (selected_names.length > 0) {
        const selected_name = selected_names[0].name;
        void setFieldValue('name', selected_name);
      }
    }
  }, [
    actorsAvailable,
    categories,
    nameSelection,
    selection,
    series,
    setFieldValue,
    studios,
  ]);
  return null;
};

const RadioSelectionChanged = () => {
  const {
    setFieldValue,
    values: { selection },
  } = useFormikContext<MoviePropertyFormValuesType>();

  useEffect(() => {
    void setFieldValue('name', '');
    void setFieldValue('nameSelection', '');
  }, [selection, setFieldValue]);
  return null;
};

const MoviePropertyForm = () => {
  const { data: actorsAvailable } = useActorsQuery();
  const { data: categories } = useCategoriesQuery();
  const { data: series } = useSeriesQuery();
  const { data: studios } = useStudiosQuery();
  const [actorAddTrigger] = useActorAddMutation();
  const [actorDeleteTrigger] = useActorDeleteMutation();
  const [actorUpdateTrigger] = useActorUpdateMutation();
  const [categoryAddTrigger] = useCategoryAddMutation();
  const [categoryDeleteTrigger] = useCategoryDeleteMutation();
  const [categoryUpdateTrigger] = useCategoryUpdateMutation();
  const [seriesAddTrigger] = useSeriesAddMutation();
  const [seriesDeleteTrigger] = useSeriesDeleteMutation();
  const [seriesUpdateTrigger] = useSeriesUpdateMutation();
  const [studioAddTrigger] = useStudioAddMutation();
  const [studioDeleteTrigger] = useStudioDeleteMutation();
  const [studioUpdateTrigger] = useStudioUpdateMutation();
  const initialValues: MoviePropertyFormValuesType = {
    action: 'add',
    name: '',
    nameSelection: '',
    selection: 'actor',
  };

  const onSubmit = async (
    { action, name, nameSelection, selection }: MoviePropertyFormValuesType,
    helpers: FormikHelpers<MoviePropertyFormValuesType>
  ) => {
    if (action === 'remove' && nameSelection === '') {
      helpers.setStatus('Please make a selection first');
      return;
    }

    const selectionTitle =
      selection.charAt(0).toUpperCase() + selection.slice(1);
    let trigger;
    let verb: 'added' | 'removed' | 'updated';
    const params = {
      id: nameSelection,
      name: name,
    };

    switch (action) {
      case 'add':
        verb = 'added';
        switch (selection) {
          case 'actor':
            trigger = actorAddTrigger;
            break;
          case 'category':
            trigger = categoryAddTrigger;
            break;
          case 'series':
            trigger = seriesAddTrigger;
            break;
          case 'studio':
            trigger = studioAddTrigger;
            break;
        }
        break;
      case 'remove':
        verb = 'removed';
        switch (selection) {
          case 'actor':
            trigger = actorDeleteTrigger;
            break;
          case 'category':
            trigger = categoryDeleteTrigger;
            break;
          case 'series':
            trigger = seriesDeleteTrigger;
            break;
          case 'studio':
            trigger = studioDeleteTrigger;
            break;
        }
        break;
      case 'update':
        verb = 'updated';
        switch (selection) {
          case 'actor':
            trigger = actorUpdateTrigger;
            break;
          case 'category':
            trigger = categoryUpdateTrigger;
            break;
          case 'series':
            trigger = seriesUpdateTrigger;
            break;
          case 'studio':
            trigger = studioUpdateTrigger;
            break;
        }
        break;
    }

    try {
      await trigger(params).unwrap();
      helpers.setStatus(`${selectionTitle} ${name} ${verb}`);
      void helpers.setFieldValue('name', '');
      if (action === 'remove') {
        void helpers.setFieldValue('nameSelection', '');
      }
    } catch (error) {
      const { status, data } = error as FetchBaseQueryError;
      if (status !== 422) {
        const {
          detail: { message },
        } = data as HTTPExceptionType;
        helpers.setStatus(message ? message : 'Unknown server error');
      }
    }
  };

  return (
    <div className="border border-solid border-black mx-auto p-4 w-max">
      <Formik initialValues={initialValues} onSubmit={onSubmit}>
        {(formik) => (
          <form onSubmit={formik.handleSubmit}>
            <NameSelectorChanged />
            <RadioSelectionChanged />
            <div className="flex flex-col md:flex-row justify-center">
              <div className="md:mr-1">
                <MoviePropertyFormSelector title="Action">
                  <label>
                    <Field
                      className="mx-2"
                      type="radio"
                      name="action"
                      value="add"
                    />
                    Add
                  </label>
                  <label>
                    <Field
                      className="mx-2"
                      type="radio"
                      name="action"
                      value="update"
                    />
                    Update
                  </label>
                  <label>
                    <Field
                      className="mx-2"
                      type="radio"
                      name="action"
                      value="remove"
                    />
                    Remove
                  </label>
                </MoviePropertyFormSelector>
              </div>
              <div className="md:ml-1">
                <MoviePropertyFormSelector title="Movie Property">
                  <label>
                    <Field
                      className="mx-1"
                      type="radio"
                      name="selection"
                      value="actor"
                    />
                    Actor
                  </label>
                  <label>
                    <Field
                      className="mx-1"
                      type="radio"
                      name="selection"
                      value="category"
                    />
                    Category
                  </label>
                  <label>
                    <Field
                      className="mx-1"
                      type="radio"
                      name="selection"
                      value="series"
                    />
                    Series
                  </label>
                  <label>
                    <Field
                      className="mx-1"
                      type="radio"
                      name="selection"
                      value="studio"
                    />
                    Studio
                  </label>
                </MoviePropertyFormSelector>
              </div>
            </div>
            {formik.values.action !== 'remove' ? (
              <div className="my-2">
                <Field
                  className="border border-solid border-gray-300 focus:border-2 focus:border-gray-100 outline-none focus:bg-gray-100 rounded p-1 mt-1 h-7 w-full"
                  type="text"
                  name="name"
                  required
                />
              </div>
            ) : (
              <div className="mt-2 p-4"></div>
            )}

            {formik.values.action !== 'add' ? (
              <div className="my-3">
                <select
                  className="w-full p-1 rounded"
                  name="nameSelection"
                  onChange={formik.handleChange}
                >
                  <option value="">None</option>
                  {formik.values.selection === 'actor' &&
                    actorsAvailable?.map((actor) => (
                      <option key={actor.id} value={actor.id}>
                        {actor.name}
                      </option>
                    ))}
                  {formik.values.selection === 'category' &&
                    categories?.map((category) => (
                      <option key={category.id} value={category.id}>
                        {category.name}
                      </option>
                    ))}
                  {formik.values.selection === 'series' &&
                    series?.map((series) => (
                      <option key={series.id} value={series.id}>
                        {series.name}
                      </option>
                    ))}
                  {formik.values.selection === 'studio' &&
                    studios?.map((studio) => (
                      <option key={studio.id} value={studio.id}>
                        {studio.name}
                      </option>
                    ))}
                </select>
              </div>
            ) : (
              <div className="mt-2 p-4"></div>
            )}
            <div className="grid mt-3">
              <button
                className="bg-green-700 hover:bg-green-600 font-semibold py-1 rounded text-white text-center tracking-wider uppercase"
                type="submit"
              >
                {formik.values.action} {formik.values.selection}
              </button>
            </div>
            {formik.status ? (
              <div className="flex flex-col mt-3 text-center">
                {formik.status}
              </div>
            ) : (
              <div className="flex flex-col mt-3 text-center">
                Please make a selection
              </div>
            )}
          </form>
        )}
      </Formik>
    </div>
  );
};

export default MoviePropertyForm;
