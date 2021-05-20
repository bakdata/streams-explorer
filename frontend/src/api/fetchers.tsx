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

export type Omit<T, K extends keyof T> = Pick<T, Exclude<keyof T, K>>;

const encodingFn = encodeURIComponent;

const encodingTagFactory = (encodingFn: typeof encodeURIComponent) => (
  strings: TemplateStringsArray,
  ...params: (string | number | boolean)[]
) =>
  strings.reduce(
    (accumulatedPath, pathPart, idx) =>
      `${accumulatedPath}${pathPart}${
        idx < params.length ? encodingFn(params[idx]) : ""
      }`,
    ""
  );

const encode = encodingTagFactory(encodingFn);

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
  value: {};
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
    path={encode`/static`}
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
  useGet<FrontendStaticGetResponse, unknown, void, void>(
    encode`/static`,
    props
  );

export interface FrontendGetResponse {}

export type FrontendGetProps = Omit<
  GetProps<FrontendGetResponse, unknown, void, void>,
  "path"
>;

/**
 * Frontend
 */
export const FrontendGet = (props: FrontendGetProps) => (
  <Get<FrontendGetResponse, unknown, void, void> path={encode`/`} {...props} />
);

export type UseFrontendGetProps = Omit<
  UseGetProps<FrontendGetResponse, unknown, void, void>,
  "path"
>;

/**
 * Frontend
 */
export const useFrontendGet = (props: UseFrontendGetProps) =>
  useGet<FrontendGetResponse, unknown, void, void>(encode`/`, props);

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
    path={encode`/api/update`}
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
    encode`/api/update`,
    props
  );

export interface GraphPositionedApiGraphGetQueryParams {
  pipeline_name?: string;
}

export type GraphPositionedApiGraphGetProps = Omit<
  GetProps<
    Graph,
    HTTPValidationError,
    GraphPositionedApiGraphGetQueryParams,
    void
  >,
  "path"
>;

/**
 * Graph Positioned
 */
export const GraphPositionedApiGraphGet = (
  props: GraphPositionedApiGraphGetProps
) => (
  <Get<Graph, HTTPValidationError, GraphPositionedApiGraphGetQueryParams, void>
    path={encode`/api/graph`}
    {...props}
  />
);

export type UseGraphPositionedApiGraphGetProps = Omit<
  UseGetProps<
    Graph,
    HTTPValidationError,
    GraphPositionedApiGraphGetQueryParams,
    void
  >,
  "path"
>;

/**
 * Graph Positioned
 */
export const useGraphPositionedApiGraphGet = (
  props: UseGraphPositionedApiGraphGetProps
) =>
  useGet<
    Graph,
    HTTPValidationError,
    GraphPositionedApiGraphGetQueryParams,
    void
  >(encode`/api/graph`, props);

export type PipelinesApiPipelinesGetProps = Omit<
  GetProps<Pipelines, unknown, void, void>,
  "path"
>;

/**
 * Pipelines
 */
export const PipelinesApiPipelinesGet = (
  props: PipelinesApiPipelinesGetProps
) => (
  <Get<Pipelines, unknown, void, void>
    path={encode`/api/pipelines`}
    {...props}
  />
);

export type UsePipelinesApiPipelinesGetProps = Omit<
  UseGetProps<Pipelines, unknown, void, void>,
  "path"
>;

/**
 * Pipelines
 */
export const usePipelinesApiPipelinesGet = (
  props: UsePipelinesApiPipelinesGetProps
) => useGet<Pipelines, unknown, void, void>(encode`/api/pipelines`, props);

export interface NodeInfoApiNodeNodeIdGetPathParams {
  node_id: string;
}

export type NodeInfoApiNodeNodeIdGetProps = Omit<
  GetProps<
    NodeInformation,
    HTTPValidationError,
    void,
    NodeInfoApiNodeNodeIdGetPathParams
  >,
  "path"
> &
  NodeInfoApiNodeNodeIdGetPathParams;

/**
 * Node Info
 */
export const NodeInfoApiNodeNodeIdGet = ({
  node_id,
  ...props
}: NodeInfoApiNodeNodeIdGetProps) => (
  <Get<
    NodeInformation,
    HTTPValidationError,
    void,
    NodeInfoApiNodeNodeIdGetPathParams
  >
    path={encode`/api/node/${node_id}`}
    {...props}
  />
);

export type UseNodeInfoApiNodeNodeIdGetProps = Omit<
  UseGetProps<
    NodeInformation,
    HTTPValidationError,
    void,
    NodeInfoApiNodeNodeIdGetPathParams
  >,
  "path"
> &
  NodeInfoApiNodeNodeIdGetPathParams;

/**
 * Node Info
 */
export const useNodeInfoApiNodeNodeIdGet = ({
  node_id,
  ...props
}: UseNodeInfoApiNodeNodeIdGetProps) =>
  useGet<
    NodeInformation,
    HTTPValidationError,
    void,
    NodeInfoApiNodeNodeIdGetPathParams
  >(
    (paramsInPath: NodeInfoApiNodeNodeIdGetPathParams) =>
      encode`/api/node/${paramsInPath.node_id}`,
    { pathParams: { node_id }, ...props }
  );

export interface LinkingApiNodeLinkingNodeIdGetQueryParams {
  link_type?: string;
}

export interface LinkingApiNodeLinkingNodeIdGetPathParams {
  node_id: string;
}

export type LinkingApiNodeLinkingNodeIdGetProps = Omit<
  GetProps<
    string,
    HTTPValidationError,
    LinkingApiNodeLinkingNodeIdGetQueryParams,
    LinkingApiNodeLinkingNodeIdGetPathParams
  >,
  "path"
> &
  LinkingApiNodeLinkingNodeIdGetPathParams;

/**
 * Linking
 */
export const LinkingApiNodeLinkingNodeIdGet = ({
  node_id,
  ...props
}: LinkingApiNodeLinkingNodeIdGetProps) => (
  <Get<
    string,
    HTTPValidationError,
    LinkingApiNodeLinkingNodeIdGetQueryParams,
    LinkingApiNodeLinkingNodeIdGetPathParams
  >
    path={encode`/api/node/linking/${node_id}`}
    {...props}
  />
);

export type UseLinkingApiNodeLinkingNodeIdGetProps = Omit<
  UseGetProps<
    string,
    HTTPValidationError,
    LinkingApiNodeLinkingNodeIdGetQueryParams,
    LinkingApiNodeLinkingNodeIdGetPathParams
  >,
  "path"
> &
  LinkingApiNodeLinkingNodeIdGetPathParams;

/**
 * Linking
 */
export const useLinkingApiNodeLinkingNodeIdGet = ({
  node_id,
  ...props
}: UseLinkingApiNodeLinkingNodeIdGetProps) =>
  useGet<
    string,
    HTTPValidationError,
    LinkingApiNodeLinkingNodeIdGetQueryParams,
    LinkingApiNodeLinkingNodeIdGetPathParams
  >(
    (paramsInPath: LinkingApiNodeLinkingNodeIdGetPathParams) =>
      encode`/api/node/linking/${paramsInPath.node_id}`,
    { pathParams: { node_id }, ...props }
  );

export type MetricsApiMetricsGetProps = Omit<
  GetProps<Metric[], unknown, void, void>,
  "path"
>;

/**
 * Metrics
 */
export const MetricsApiMetricsGet = (props: MetricsApiMetricsGetProps) => (
  <Get<Metric[], unknown, void, void> path={encode`/api/metrics`} {...props} />
);

export type UseMetricsApiMetricsGetProps = Omit<
  UseGetProps<Metric[], unknown, void, void>,
  "path"
>;

/**
 * Metrics
 */
export const useMetricsApiMetricsGet = (props: UseMetricsApiMetricsGetProps) =>
  useGet<Metric[], unknown, void, void>(encode`/api/metrics`, props);
