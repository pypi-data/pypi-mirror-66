#!/usr/bin/env python3
from pdaltagent.tasks import send_to_pd
from argparse import ArgumentParser
import time

def build_queue_arg_parser(description):

    parser = ArgumentParser(description=description)
    parser.add_argument(
        "-k", "--routing-key", dest="routing_key", required=True,
        help="Event routing key Key"
        )
    parser.add_argument(
        "-t", "--event-type", dest="event_type", required=True,
        choices=["trigger", "acknowledge", "resolve"],
        help="Event type"
        )
    parser.add_argument(
        "-s", "--severity", dest="severity",
        choices=["critical", "error", "warning", "info"],
        help="Severity",
        default="critical"
        )
    parser.add_argument(
        "-o", "--source", dest="source",
        help="Source",
        default="PDAltagent"
        )
    parser.add_argument(
        "-m", "--component", dest="component",
        help="Component"
        )
    parser.add_argument(
        "-g", "--group", dest="group",
        help="Group"
        )
    parser.add_argument(
        "-l", "--class", dest="event_class",
        help="Class"
        )
    parser.add_argument(
        "-d", "--description", dest="description",
        help="Short description of the problem"
        )
    parser.add_argument(
        "-i", "--incident-key", dest="incident_key",
        help="Incident Key"
        )
    parser.add_argument(
        "-c", "--client", dest="client",
        help="Client"
        )
    parser.add_argument(
        "-u", "--client-url", dest="client_url",
        help="Client URL"
        )
    parser.add_argument(
        "-f", "--field", action="append", dest="fields",
        help="Add given KEY=VALUE pair to the event details"
        )
    parser.add_argument(
        "-q", "--quiet", action="store_true", dest="quiet",
        help="Operate quietly (no output)"
        )
    return parser

def parse_fields(fields):
    if fields is None:
        return {}
    return dict(f.split("=", 1) for f in fields)

def main():
    print(f"{time.time()} start main")
    description = "Queue up a trigger, acknowledge, or resolve event to PagerDuty."
    parser = build_queue_arg_parser(description)
    args = parser.parse_args()

    if args.event_type == "trigger":
        if (not args.description) or (not args.description.strip()):
            parser.error("Event type '%s' requires description" % args.event_type)
    else:
        if not args.incident_key:
            parser.error("Event type '%s' requires incident key" % args.event_type)

    body = {
        "routing_key": args.routing_key,
        "event_action": args.event_type,
    }
    if args.incident_key:
        body["dedup_key"] = args.incident_key

    if args.event_type == "trigger":
        custom_details = parse_fields(args.fields)
        body["payload"] = {
            "summary": args.description,
            "severity": args.severity,
            "custom_details": custom_details
        }
        if args.client:
            body["client"] = args.client
        if args.client_url:
            body["client_url"] = args.client_url
        if args.source:
            body["payload"]["source"] = args.source
        if args.component:
            body["payload"]["component"] = args.component
        if args.group:
            body["payload"]["group"] = args.group
        if args.event_class:
            body["payload"]["class"] = args.event_class

    print(f"{time.time()} send to pd")
    send_to_pd.delay(args.routing_key, body)
    print(f"{time.time()} done\n\n")

if __name__ == '__main__':
    main()