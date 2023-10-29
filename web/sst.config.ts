import { SSTConfig } from "sst";
import { NextjsSite } from "sst/constructs";
import { Certificate } from "aws-cdk-lib/aws-certificatemanager";

export default {
  config(_input) {
    return {
      name: "kodiko",
      region: process.env.REGION || "",
    };
  },
  stacks(app) {
    app.stack(function Site({ stack }) {
      const site = new NextjsSite(stack, "site", {
        customDomain: {
          domainName: process.env.DOMAIN_NAME || "",
          hostedZone: process.env.HOSTED_ZONE_NAME || "",
          cdk: {
            certificate: Certificate.fromCertificateArn(
              stack,
              "MyCert",
              // create certificate in us-east-1 region for cloudfront
              process.env.CERT_ARN || ""
            ),
          },
        },
      });

      stack.addOutputs({
        SiteUrl: site.url,
      });
    });
  },
} satisfies SSTConfig;
