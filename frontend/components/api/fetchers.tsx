/* Generated by restful-react */

import React from "react";
import {
  Get,
  GetProps,
  useGet,
  UseGetProps,
  Mutate,
  MutateProps,
  useMutate,
  UseMutateProps,
} from "restful-react";
export const SPEC_VERSION = "0.1.0";
export interface Edge {
  source: string;
  target: string;
}

export interface Graph {
  directed: boolean;
  multigraph: boolean;
  graph?: {};
  nodes: Node[];
  edges: Edge[];
}

export interface HTTPValidationError {
  detail?: ValidationError[];
}

export interface Icon {
  img: string;
  show: boolean;
  width: number;
  height: number;
}

export interface Metric {
  node_id: string;
  messages_in?: number;
  messages_out?: number;
  consumer_lag?: number;
  consumer_read_rate?: number;
  topic_size?: number;
  replicas?: number;
  replicas_available?: number;
  connector_tasks?: number;
}

export interface Node {
  id: string;
  label: string;
  node_type: string;
  icon?: Icon;
  x?: number;
  y?: number;
}

export interface NodeInfoListItem {
  name: string;
  value: string | { [key: string]: any };
  type: NodeInfoType;
}

/**
 * An enumeration.
 */
export type NodeInfoType = "json" | "basic" | "link";

export interface NodeInformation {
  node_id: string;
  node_type: NodeTypesEnum;
  info: NodeInfoListItem[];
}

/**
 * An enumeration.
 */
export type NodeTypesEnum =
  | "streaming-app"
  | "connector"
  | "topic"
  | "error-topic"
  | "sink/source";

export interface Pipelines {
  pipelines: string[];
}

export interface ValidationError {
  loc: string[];
  msg: string;
  type: string;
}

export interface FrontendStaticGetResponse {}

export type FrontendStaticGetProps = Omit<
  GetProps<FrontendStaticGetResponse, unknown, void, void>,
  "path"
>;

/**
 * Frontend
 */
export const FrontendStaticGet = (props: FrontendStaticGetProps) => (
  <Get<FrontendStaticGetResponse, unknown, void, void>
    path={`/static`}
    {...props}
  />
);

export type UseFrontendStaticGetProps = Omit<
  UseGetProps<FrontendStaticGetResponse, unknown, void, void>,
  "path"
>;

/**
 * Frontend
 */
export const useFrontendStaticGet = (props: UseFrontendStaticGetProps) =>
  useGet<FrontendStaticGetResponse, unknown, void, void>(`/static`, props);

export interface FrontendGetResponse {}

export type FrontendGetProps = Omit<
  GetProps<FrontendGetResponse, unknown, void, void>,
  "path"
>;

/**
 * Frontend
 */
export const FrontendGet = (props: FrontendGetProps) => (
  <Get<FrontendGetResponse, unknown, void, void> path={`/`} {...props} />
);

export type UseFrontendGetProps = Omit<
  UseGetProps<FrontendGetResponse, unknown, void, void>,
  "path"
>;

/**
 * Frontend
 */
export const useFrontendGet = (props: UseFrontendGetProps) =>
  useGet<FrontendGetResponse, unknown, void, void>(`/`, props);

export interface UpdateApiUpdatePostResponse {}

export type UpdateApiUpdatePostProps = Omit<
  MutateProps<UpdateApiUpdatePostResponse, unknown, void, void, void>,
  "path" | "verb"
>;

/**
 * Update
 */
export const UpdateApiUpdatePost = (props: UpdateApiUpdatePostProps) => (
  <Mutate<UpdateApiUpdatePostResponse, unknown, void, void, void>
    verb="POST"
    path={`/api/update`}
    {...props}
  />
);

export type UseUpdateApiUpdatePostProps = Omit<
  UseMutateProps<UpdateApiUpdatePostResponse, unknown, void, void, void>,
  "path" | "verb"
>;

/**
 * Update
 */
export const useUpdateApiUpdatePost = (props: UseUpdateApiUpdatePostProps) =>
  useMutate<UpdateApiUpdatePostResponse, unknown, void, void, void>(
    "POST",
    `/api/update`,
    props
  );

export interface GetPositionedGraphApiGraphGetQueryParams {
  pipeline_name?: string;
}

export type GetPositionedGraphApiGraphGetProps = Omit<
  GetProps<
    Graph,
    HTTPValidationError,
    GetPositionedGraphApiGraphGetQueryParams,
    void
  >,
  "path"
>;

/**
 * Get Positioned Graph
 */
export const GetPositionedGraphApiGraphGet = (
  props: GetPositionedGraphApiGraphGetProps
) => (
  <Get<
    Graph,
    HTTPValidationError,
    GetPositionedGraphApiGraphGetQueryParams,
    void
  >
    path={`/api/graph`}
    {...props}
  />
);

export type UseGetPositionedGraphApiGraphGetProps = Omit<
  UseGetProps<
    Graph,
    HTTPValidationError,
    GetPositionedGraphApiGraphGetQueryParams,
    void
  >,
  "path"
>;

/**
 * Get Positioned Graph
 */
export const useGetPositionedGraphApiGraphGet = (
  props: UseGetPositionedGraphApiGraphGetProps
) =>
  useGet<
    Graph,
    HTTPValidationError,
    GetPositionedGraphApiGraphGetQueryParams,
    void
  >(`/api/graph`, props);

export type GetPipelinesApiPipelinesGetProps = Omit<
  GetProps<Pipelines, unknown, void, void>,
  "path"
>;

/**
 * Get Pipelines
 */
export const GetPipelinesApiPipelinesGet = (
  props: GetPipelinesApiPipelinesGetProps
) => <Get<Pipelines, unknown, void, void> path={`/api/pipelines`} {...props} />;

export type UseGetPipelinesApiPipelinesGetProps = Omit<
  UseGetProps<Pipelines, unknown, void, void>,
  "path"
>;

/**
 * Get Pipelines
 */
export const useGetPipelinesApiPipelinesGet = (
  props: UseGetPipelinesApiPipelinesGetProps
) => useGet<Pipelines, unknown, void, void>(`/api/pipelines`, props);

export interface GetNodeInfoApiNodeNodeIdGetPathParams {
  node_id: string;
}

export type GetNodeInfoApiNodeNodeIdGetProps = Omit<
  GetProps<
    NodeInformation,
    HTTPValidationError,
    void,
    GetNodeInfoApiNodeNodeIdGetPathParams
  >,
  "path"
> &
  GetNodeInfoApiNodeNodeIdGetPathParams;

/**
 * Get Node Info
 */
export const GetNodeInfoApiNodeNodeIdGet = ({
  node_id,
  ...props
}: GetNodeInfoApiNodeNodeIdGetProps) => (
  <Get<
    NodeInformation,
    HTTPValidationError,
    void,
    GetNodeInfoApiNodeNodeIdGetPathParams
  >
    path={`/api/node/${node_id}`}
    {...props}
  />
);

export type UseGetNodeInfoApiNodeNodeIdGetProps = Omit<
  UseGetProps<
    NodeInformation,
    HTTPValidationError,
    void,
    GetNodeInfoApiNodeNodeIdGetPathParams
  >,
  "path"
> &
  GetNodeInfoApiNodeNodeIdGetPathParams;

/**
 * Get Node Info
 */
export const useGetNodeInfoApiNodeNodeIdGet = ({
  node_id,
  ...props
}: UseGetNodeInfoApiNodeNodeIdGetProps) =>
  useGet<
    NodeInformation,
    HTTPValidationError,
    void,
    GetNodeInfoApiNodeNodeIdGetPathParams
  >(
    (paramsInPath: GetNodeInfoApiNodeNodeIdGetPathParams) =>
      `/api/node/${paramsInPath.node_id}`,
    { pathParams: { node_id }, ...props }
  );

export interface GetNodeSchemaVersionsApiNodeNodeIdSchemaGetPathParams {
  node_id: string;
}

export type GetNodeSchemaVersionsApiNodeNodeIdSchemaGetProps = Omit<
  GetProps<
    number[],
    HTTPValidationError,
    void,
    GetNodeSchemaVersionsApiNodeNodeIdSchemaGetPathParams
  >,
  "path"
> &
  GetNodeSchemaVersionsApiNodeNodeIdSchemaGetPathParams;

/**
 * Get Node Schema Versions
 */
export const GetNodeSchemaVersionsApiNodeNodeIdSchemaGet = ({
  node_id,
  ...props
}: GetNodeSchemaVersionsApiNodeNodeIdSchemaGetProps) => (
  <Get<
    number[],
    HTTPValidationError,
    void,
    GetNodeSchemaVersionsApiNodeNodeIdSchemaGetPathParams
  >
    path={`/api/node/${node_id}/schema`}
    {...props}
  />
);

export type UseGetNodeSchemaVersionsApiNodeNodeIdSchemaGetProps = Omit<
  UseGetProps<
    number[],
    HTTPValidationError,
    void,
    GetNodeSchemaVersionsApiNodeNodeIdSchemaGetPathParams
  >,
  "path"
> &
  GetNodeSchemaVersionsApiNodeNodeIdSchemaGetPathParams;

/**
 * Get Node Schema Versions
 */
export const useGetNodeSchemaVersionsApiNodeNodeIdSchemaGet = ({
  node_id,
  ...props
}: UseGetNodeSchemaVersionsApiNodeNodeIdSchemaGetProps) =>
  useGet<
    number[],
    HTTPValidationError,
    void,
    GetNodeSchemaVersionsApiNodeNodeIdSchemaGetPathParams
  >(
    (paramsInPath: GetNodeSchemaVersionsApiNodeNodeIdSchemaGetPathParams) =>
      `/api/node/${paramsInPath.node_id}/schema`,
    { pathParams: { node_id }, ...props }
  );

export interface GetNodeSchemaApiNodeNodeIdSchemaVersionGetResponse {
  [key: string]: any;
}

export interface GetNodeSchemaApiNodeNodeIdSchemaVersionGetPathParams {
  node_id: string;
  version: number;
}

export type GetNodeSchemaApiNodeNodeIdSchemaVersionGetProps = Omit<
  GetProps<
    GetNodeSchemaApiNodeNodeIdSchemaVersionGetResponse,
    HTTPValidationError,
    void,
    GetNodeSchemaApiNodeNodeIdSchemaVersionGetPathParams
  >,
  "path"
> &
  GetNodeSchemaApiNodeNodeIdSchemaVersionGetPathParams;

/**
 * Get Node Schema
 */
export const GetNodeSchemaApiNodeNodeIdSchemaVersionGet = ({
  node_id,
  version,
  ...props
}: GetNodeSchemaApiNodeNodeIdSchemaVersionGetProps) => (
  <Get<
    GetNodeSchemaApiNodeNodeIdSchemaVersionGetResponse,
    HTTPValidationError,
    void,
    GetNodeSchemaApiNodeNodeIdSchemaVersionGetPathParams
  >
    path={`/api/node/${node_id}/schema/${version}`}
    {...props}
  />
);

export type UseGetNodeSchemaApiNodeNodeIdSchemaVersionGetProps = Omit<
  UseGetProps<
    GetNodeSchemaApiNodeNodeIdSchemaVersionGetResponse,
    HTTPValidationError,
    void,
    GetNodeSchemaApiNodeNodeIdSchemaVersionGetPathParams
  >,
  "path"
> &
  GetNodeSchemaApiNodeNodeIdSchemaVersionGetPathParams;

/**
 * Get Node Schema
 */
export const useGetNodeSchemaApiNodeNodeIdSchemaVersionGet = ({
  node_id,
  version,
  ...props
}: UseGetNodeSchemaApiNodeNodeIdSchemaVersionGetProps) =>
  useGet<
    GetNodeSchemaApiNodeNodeIdSchemaVersionGetResponse,
    HTTPValidationError,
    void,
    GetNodeSchemaApiNodeNodeIdSchemaVersionGetPathParams
  >(
    (paramsInPath: GetNodeSchemaApiNodeNodeIdSchemaVersionGetPathParams) =>
      `/api/node/${paramsInPath.node_id}/schema/${paramsInPath.version}`,
    { pathParams: { node_id, version }, ...props }
  );

export interface GetLinkingApiNodeLinkingNodeIdGetQueryParams {
  link_type?: string;
}

export interface GetLinkingApiNodeLinkingNodeIdGetPathParams {
  node_id: string;
}

export type GetLinkingApiNodeLinkingNodeIdGetProps = Omit<
  GetProps<
    string,
    HTTPValidationError,
    GetLinkingApiNodeLinkingNodeIdGetQueryParams,
    GetLinkingApiNodeLinkingNodeIdGetPathParams
  >,
  "path"
> &
  GetLinkingApiNodeLinkingNodeIdGetPathParams;

/**
 * Get Linking
 */
export const GetLinkingApiNodeLinkingNodeIdGet = ({
  node_id,
  ...props
}: GetLinkingApiNodeLinkingNodeIdGetProps) => (
  <Get<
    string,
    HTTPValidationError,
    GetLinkingApiNodeLinkingNodeIdGetQueryParams,
    GetLinkingApiNodeLinkingNodeIdGetPathParams
  >
    path={`/api/node/linking/${node_id}`}
    {...props}
  />
);

export type UseGetLinkingApiNodeLinkingNodeIdGetProps = Omit<
  UseGetProps<
    string,
    HTTPValidationError,
    GetLinkingApiNodeLinkingNodeIdGetQueryParams,
    GetLinkingApiNodeLinkingNodeIdGetPathParams
  >,
  "path"
> &
  GetLinkingApiNodeLinkingNodeIdGetPathParams;

/**
 * Get Linking
 */
export const useGetLinkingApiNodeLinkingNodeIdGet = ({
  node_id,
  ...props
}: UseGetLinkingApiNodeLinkingNodeIdGetProps) =>
  useGet<
    string,
    HTTPValidationError,
    GetLinkingApiNodeLinkingNodeIdGetQueryParams,
    GetLinkingApiNodeLinkingNodeIdGetPathParams
  >(
    (paramsInPath: GetLinkingApiNodeLinkingNodeIdGetPathParams) =>
      `/api/node/linking/${paramsInPath.node_id}`,
    { pathParams: { node_id }, ...props }
  );

export type GetMetricsApiMetricsGetProps = Omit<
  GetProps<Metric[], unknown, void, void>,
  "path"
>;

/**
 * Get Metrics
 */
export const GetMetricsApiMetricsGet = (
  props: GetMetricsApiMetricsGetProps
) => <Get<Metric[], unknown, void, void> path={`/api/metrics`} {...props} />;

export type UseGetMetricsApiMetricsGetProps = Omit<
  UseGetProps<Metric[], unknown, void, void>,
  "path"
>;

/**
 * Get Metrics
 */
export const useGetMetricsApiMetricsGet = (
  props: UseGetMetricsApiMetricsGetProps
) => useGet<Metric[], unknown, void, void>(`/api/metrics`, props);
