FROM opentripplanner/opentripplanner:latest

WORKDIR /var/opentripplanner

COPY router-config.json /var/opentripplanner/router-config.json
COPY graph.obj /var/opentripplanner/graph.obj

CMD ["--load", "--serve"]
