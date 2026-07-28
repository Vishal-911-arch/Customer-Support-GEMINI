class CurveValidator:

    def validate(

            self,

            curves

    ):

        final=[]

        idx=1

        for c in curves:

            pts = c["points"]

            if len(pts)<60:
                continue

            xs=[p[0] for p in pts]

            ys=[p[1] for p in pts]

            w=max(xs)-min(xs)

            h=max(ys)-min(ys)

            if w<20 and h<20:
                continue

            c["id"]=idx

            final.append(c)

            idx += 1

        return final