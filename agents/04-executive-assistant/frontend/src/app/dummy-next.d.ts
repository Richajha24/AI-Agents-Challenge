declare module "next/link" {
    const Link: any;
    export default Link;
}

declare module "next" {
    const anyExport: any;
    export default anyExport;
}

declare namespace JSX {
    interface IntrinsicElements {
        [elemName: string]: any;
    }
}

