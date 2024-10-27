import { useState } from 'react';
import { HTTPExceptionType, MovieFileType } from '../types/api';
import { useMoviesImportMutation } from '../state/MovieManagerApi';
import { FetchBaseQueryError } from '@reduxjs/toolkit/query';

const MovieImportButton = () => {
  const [importStatus, setImportStatus] = useState('');
  const [trigger] = useMoviesImportMutation();

  const onImportMovies = async () => {
    try {
      const data: MovieFileType[] = await trigger().unwrap();
      let count: number;
      if (Array.isArray(data)) {
        count = data.length;
      } else {
        count = 0;
      }
      if (count === 0) {
        setImportStatus('No movie files found');
      } else {
        setImportStatus(`Imported ${count} file${count > 1 ? 's' : ''}`);
      }
    } catch (error) {
      const { status, data } = error as FetchBaseQueryError;
      if (status !== 422) {
        const {
          detail: { message },
        } = data as HTTPExceptionType;
        setImportStatus(message ? message : 'Unknown Error');
      }
    }
  };
  return (
    <div className="border border-solid border-black p-4 my-4 mx-auto w-max">
      <div className="flex justify-center">
        <button
          className="bg-blue-500 hover:bg-blue-400 rounded py-2 px-8 text-white text-center text-lg font-semibold"
          type="button"
          onClick={() => {
            void onImportMovies();
          }}
        >
          Import Movies
        </button>
      </div>
      {importStatus ? (
        <div className="pt-3 text-center">{importStatus}</div>
      ) : (
        <div className="pt-3 text-center">Click to import movies</div>
      )}
    </div>
  );
};

export default MovieImportButton;
