"""
Command line interface for punits
"""

__version__ = "0.0.2"
__author__ = "Julin S"

import argparse

import punits

SUPPORTED_MEASURES = ['mass', 'length', 'volume', 'data', 'temperature']

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="punits",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="A punits description for argparse"
    )
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s ' + __version__
    )

    # Type conversion is automatic when `type` arg is mentioned
    parser.add_argument('measure', choices=SUPPORTED_MEASURES)
    parser.add_argument('src_unit')
    parser.add_argument('values', nargs='+', type=float)
    parser.add_argument('target_unit')
    parser.add_argument('-p', '--precision', default=2, type=int)
    parser.add_argument('-v', '--verbose', action="store_true")

    # Relevant only for length
    parser.add_argument('--dpi', type=int,
                        help="Use when converting to or from px")

    args = parser.parse_args()

    try:
        src_unit = punits.find_unit_code(args.measure, args.src_unit)
        target_unit = punits.find_unit_code(args.measure, args.target_unit)

        params = {}
        if args.dpi is not None:
            params['dpi'] = args.dpi

        results = punits.punits(args.measure, src_unit,
                                target_unit, args.values, params)
        str_results = [
            f"{round(result, args.precision):g}" for result in results]
        out_str = ' '.join(str_results)
        print(out_str)

        if args.verbose:
            factor = punits.get_factor(args.measure, src_unit, target_unit)
            if factor is not None:
                # Linear relationship between units
                print(f"\n1 {target_unit} = {factor:g} {src_unit} (approx)")
    except punits.UnknownUnitException as unknown:
        print(f"Gee.. I don't know about '{unknown.unit_name}'..")
    except punits.MissingParameterException as missing:
        print(f"Missing parameter: {missing.missing_param}")


# short form of `measure` argument to argparse
