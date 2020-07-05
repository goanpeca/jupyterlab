import { URLExt } from '@jupyterlab/coreutils';

import { ServerConnection } from '@jupyterlab/services';

import { DataConnector, IDataConnector } from '@jupyterlab/statedb';

import { Token } from '@lumino/coreutils';

/**
 * Call the API extension
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
export async function requestAPI<T>(
  locale = '',
  init: RequestInit = {}
): Promise<T> {
  // Make request to Jupyter API
  const settings = ServerConnection.makeSettings();
  const requestUrl = URLExt.join(
    settings.baseUrl,
    '/lab/api/translations/', // API Namespace
    locale
  );

  console.log(requestUrl);

  let response: Response;
  try {
    response = await ServerConnection.makeRequest(requestUrl, init, settings);
  } catch (error) {
    throw new ServerConnection.NetworkError(error);
  }

  let data: any = await response.text();

  if (data.length > 0) {
    try {
      data = JSON.parse(data);
    } catch (error) {
      console.log('Not a JSON response body.', response);
    }
  }

  if (!response.ok) {
    throw new ServerConnection.ResponseError(response, data.message || data);
  }

  return data;
}

/* 
 * Translation
 */
type Language = { [key: string]: string };

export interface ITranslatorConnector
  extends IDataConnector<
    Language,
    Language,
    { language: string }
  > {}

export const ITranslatorConnector = new Token<ITranslatorConnector>("@jupyterlab/translation:ITranslatorConnector");

export class TranslatorConnector
  extends DataConnector<
    Language,
    Language,
    { language: string }
  >
  implements ITranslatorConnector {
  async fetch(opts: { language: string }): Promise<Language> {
    return requestAPI(opts.language);
  }
}

// See: http://messageformat.github.io/Jed/
export type LanguageBundle = {
  gettext(key: string): string,
  ngettext(singular_key: string, plural_key: string, n: number): string,
  sprintf(...args: any[]): string
};

export interface ITranslator {
  load(domain: string): LanguageBundle;
}

export const ITranslator = new Token<ITranslator>('@jupyterlab/translation:ITranslator');
